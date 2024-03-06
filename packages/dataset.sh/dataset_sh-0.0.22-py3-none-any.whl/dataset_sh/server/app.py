import binascii
import json
import os
from functools import wraps

import jwt
from flask import Flask, jsonify, send_file, g, request, make_response
from head_switcher import install_to_flask, load_from_package_resources

from dataset_sh.clients import LocalStorage
from dataset_sh.utils.files import filesize
from werkzeug.security import safe_join

from dataset_sh.server.config import load_config
from dataset_sh.server.project_file_manager import ProjectArticleManager
from dataset_sh.server.utils import generate_download_code
from .core import RepoServerConfig
from .constants import ACCESS_KEY_HEADER_NAME, TOKEN_HEADER_KEY


def load_frontend_assets():
    try:
        return load_from_package_resources('dataset_sh.server.assets', 'app-ui.frontend')
    except FileNotFoundError as e:
        return {
            'index.html': 'dataset.sh web interface is disabled.'
        }


DISABLE_UI = os.environ.get('DISABLE_DATASET_APP_UI', '0').lower() in ['true', '1']


def create_app(frontend_assets=None, config: RepoServerConfig = None):
    app = Flask(__name__, static_folder=None)

    if config is None:
        config = load_config(app).override_from_env()

    if frontend_assets is None:
        if not DISABLE_UI:
            frontend_assets = load_frontend_assets()
        else:
            frontend_assets = {
                'index.html': "dataset.sh web ui is disabled"
            }

    config.make_dirs()

    local_storage = LocalStorage(config.data_folder)
    pf_manager = ProjectArticleManager(config.article_folder)

    @app.route('/api/version', methods=['GET'])
    def get_server_version():
        return jsonify({'version': '0.0.5'})

    if config.require_auth:
        @app.route('/api/login', methods=['POST'])
        def login():
            username = request.json.get('username')
            password = request.json.get('password')
            if config.verify_userpass(username, password):
                token = jwt.encode({
                    'username': username
                }, config.secret, algorithm="HS256")
                response = make_response(jsonify({'message': 'Login successful'}))
                response.set_cookie(TOKEN_HEADER_KEY, token)
                return response
            else:
                return '', 401

        @app.route('/api/logout', methods=['POST'])
        def logout():
            response = make_response(jsonify({'message': 'Logout successful'}))
            response.delete_cookie(TOKEN_HEADER_KEY)
            return response

    @app.before_request
    def before_request_func():

        g.current_user = None
        token = request.cookies.get(TOKEN_HEADER_KEY, None)
        if token:
            try:
                payload = jwt.decode(token, config.secret, algorithms=['HS256'])
                g.current_user = payload['username']
            except jwt.ExpiredSignatureError:  # pragma: no cover
                pass
            except jwt.InvalidTokenError:  # pragma: no cover
                pass
        else:
            access_key = request.headers.get(ACCESS_KEY_HEADER_NAME, None)
            if access_key is not None:
                try:
                    g.current_user = config.verify_key(access_key)
                except (json.decoder.JSONDecodeError, binascii.Error):
                    pass

    def require_auth(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if config.require_auth and g.current_user is None:
                return '', 401
            return f(*args, **kwargs)

        return decorated_function

    @app.route('/api/info', methods=['GET'])
    @require_auth
    def get_info():
        if g.current_user is None:
            return jsonify({'username': ''})
        else:
            return jsonify({'username': g.current_user})

    @app.route('/api/hostname', methods=['GET'])
    @require_auth
    def get_host():
        return jsonify({'hostname': config.hostname})

    @app.route('/api/dataset', methods=['GET'])
    @require_auth
    def list_datasets():
        items = local_storage.datasets()
        return jsonify({
            'items': [{
                'namespace': item.namespace,
                'dataset': item.dataset_name,
            } for item in items]
        }), 200

    @app.route('/api/namespace', methods=['GET'])
    @require_auth
    def list_namespaces():
        items = local_storage.namespaces()
        return jsonify({
            'namespaces': [item.namespace for item in items]
        }), 200

    @app.route('/api/dataset/<namespace>', methods=['GET'])
    @require_auth
    def list_datasets_in_store(namespace):
        items = local_storage.namespace(namespace).datasets()
        return jsonify({
            'items': [{
                'namespace': item.namespace,
                'dataset': item.dataset_name,
            } for item in items]
        }), 200

    @app.route('/api/dataset/<namespace>/<dataset_name>/version', methods=['GET'])
    @require_auth
    def list_dataset_versions(namespace, dataset_name):
        versions = local_storage.namespace(namespace).dataset(dataset_name).versions()
        return jsonify({
            'items': [{
                "version": v.version
            } for v in versions]
        })

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag', methods=['GET'])
    @require_auth
    def list_dataset_tags(namespace, dataset_name):
        tags = local_storage.namespace(namespace).dataset(dataset_name).tags()
        return jsonify({
            'items': [{'tag': tag, 'version': version} for tag, version in tags.items()]
        })

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>', methods=['GET'])
    @require_auth
    def get_tag(namespace, dataset_name, tag):
        t = local_storage.namespace(namespace).dataset(dataset_name).resolve_tag(tag)
        if t:
            return jsonify({
                'tag': tag,
                'version': t
            })
        else:
            return '', 404

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>', methods=['POST'])
    @require_auth
    def set_tag(namespace, dataset_name, tag):

        if not config.allow_upload:
            return '', 401

        if not hasattr(g, 'current_user') or g.current_user != namespace:
            return '', 401

        local_storage.namespace(namespace).dataset(dataset_name).set_tag(tag, request.json.get('version'))
        return '', 204

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>', methods=['DELETE'])
    @require_auth
    def remove_tag(namespace, dataset_name, tag):
        if not config.allow_upload:
            return '', 401

        if not hasattr(g, 'current_user') or g.current_user != namespace:
            return '', 401
        local_storage.namespace(namespace).dataset(dataset_name).remove_tag(tag)
        return '', 204

    #
    #
    #
    #
    #  By Version
    #
    #
    #
    #
    @app.route('/api/dataset/<namespace>/<dataset_name>/version/<version>/meta', methods=['GET'])
    @require_auth
    def get_dataset_meta_by_version(namespace, dataset_name, version):
        dv = local_storage.namespace(namespace).dataset(dataset_name).version(version)
        if dv.exists():
            meta = dv.meta()
            fp = dv.datafile()
            meta['fileSize'] = filesize(fp)
            return jsonify(meta), 200
        else:
            return '', 404

    @app.route('/api/dataset/<namespace>/<dataset_name>/version/<version>', methods=['DELETE'])
    @require_auth
    def r_remove_dataset_version(namespace, dataset_name, version):
        if not config.allow_upload:
            return '', 401
        if not hasattr(g, 'current_user') or g.current_user != namespace:
            return '', 401

        dv = local_storage.namespace(namespace).dataset(dataset_name).version(version)
        if dv.exists():
            dv.delete()
            return '', 204
        else:
            return '', 404

    @app.route('/api/dataset/<namespace>/<dataset_name>/version/<version>/collection/<collection_name>/sample',
               methods=['GET'])
    @require_auth
    def get_collection_sample_by_version(namespace, dataset_name, version, collection_name):
        sample = local_storage.namespace(namespace).dataset(dataset_name).version(version).sample(collection_name)
        return jsonify(sample), 200

    @app.route('/api/dataset/<namespace>/<dataset_name>/version/<version>/collection/<collection_name>/code',
               methods=['GET'])
    @require_auth
    def get_collection_code_by_version(namespace, dataset_name, version, collection_name):
        code = local_storage.namespace(namespace).dataset(dataset_name).version(version).usage_code(collection_name)
        return {'code': code}, 200

    @app.route('/api/dataset/<namespace>/<dataset_name>/version/<version>/download-code', methods=['GET'])
    @require_auth
    def get_download_code_by_version(namespace, dataset_name, version):
        fullname = f"{namespace}/{dataset_name}"
        lang = request.values.get('lang', 'python')
        code = generate_download_code(lang, config.hostname, fullname, version=version)
        return {'code': code}, 200

    @app.route('/api/dataset/<namespace>/<dataset_name>/version/<version>/file', methods=['GET'])
    @require_auth
    def get_dataset_file_by_version(namespace, dataset_name, version):
        dv = local_storage.namespace(namespace).dataset(dataset_name).version(version)
        if dv.exists():
            f = dv.datafile()
            if os.path.exists(f):
                root = os.path.normpath(local_storage.location)
                f = os.path.normpath(f)
                if f.startswith(root):
                    return send_file(
                        f,
                        as_attachment=True,
                        download_name=f"{namespace}_{dataset_name}.dataset"
                    )
        return '', 404

    #
    #
    #
    #
    #  By Tag
    #
    #
    #
    #
    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>/meta', methods=['GET'])
    @require_auth
    def get_dataset_meta_by_tag(namespace, dataset_name, tag):
        dv = local_storage.namespace(namespace).dataset(dataset_name).tag(tag, allow_none=True)
        if dv and dv.exists():
            meta = dv.meta()
            fp = dv.datafile()
            meta['fileSize'] = filesize(fp)
            return jsonify(meta), 200
        else:
            return '', 404

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>/collection/<collection_name>/sample',
               methods=['GET'])
    @require_auth
    def get_collection_sample_by_tag(namespace, dataset_name, tag, collection_name):
        dv = local_storage.namespace(namespace).dataset(dataset_name).tag(tag, allow_none=True)
        if dv and dv.exists():
            sample = dv.sample(collection_name)
            return jsonify(sample), 200
        else:
            return "", 404

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>/collection/<collection_name>/code',
               methods=['GET'])
    @require_auth
    def get_collection_code_by_tag(namespace, dataset_name, tag, collection_name):
        dv = local_storage.namespace(namespace).dataset(dataset_name).tag(tag, allow_none=True)
        if dv and dv.exists():
            code = dv.usage_code(collection_name)
            return jsonify({'code': code}), 200
        else:
            return "", 404

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>/download-code', methods=['GET'])
    @require_auth
    def get_download_code_by_tag(namespace, dataset_name, tag):
        fullname = f"{namespace}/{dataset_name}"
        lang = request.values.get('lang', 'python')
        code = generate_download_code(lang, config.hostname, fullname, tag=tag)
        return {'code': code}, 200

    @app.route('/api/dataset/<namespace>/<dataset_name>/tag/<tag>/file', methods=['GET'])
    @require_auth
    def get_dataset_file_by_tag(namespace, dataset_name, tag):
        dv = local_storage.namespace(namespace).dataset(dataset_name).tag(tag, allow_none=True)
        if dv and dv.exists():
            f = dv.datafile()
            if os.path.exists(f):
                root = os.path.normpath(local_storage.location)
                f = os.path.normpath(f)
                if f.startswith(root):
                    return send_file(
                        f,
                        as_attachment=True,
                        download_name=f"{namespace}_{dataset_name}.dataset"
                    )
        return '', 404

    #
    #
    #
    #
    #  Upload Dataset
    #
    #
    #
    #
    @app.route('/api/dataset/<namespace>/<dataset_name>', methods=['POST'])
    @require_auth
    def create_dataset(namespace, dataset_name):
        if config.allow_upload:
            user_name = namespace
            dataset_name = dataset_name
            tags = [t.strip() for t in request.args.get('tag', '').split(',') if t.strip() != '']

            if not hasattr(g, 'current_user') or g.current_user != user_name:
                return '', 401

            os.makedirs(safe_join(config.uploader_folder, user_name, dataset_name), exist_ok=True)
            fp = safe_join(config.uploader_folder, user_name, dataset_name, 'dataset_file')
            uploaded_files = request.files.getlist("file")  # "file" is the name attribute in your HTML form
            uploaded_file = uploaded_files[0]

            if uploaded_file.filename == 'dataset-sh-file':
                uploaded_file.save(fp)
                version_hex = local_storage.namespace(namespace).dataset(dataset_name).import_file(
                    fp,
                    remove_source=True,
                    tags=tags
                )
                return '', 204

            return '', 400
        else:
            return '', 401

    #
    #
    #
    #
    #  Articles
    #
    #
    #
    #
    @app.route('/api/post-assets/<path:asset_path>', methods=['GET'])
    @require_auth
    def get_asset_path(asset_path):
        fp = os.path.join(
            pf_manager.base_folder,
            '__assets__',
            asset_path
        )

        fp = os.path.normpath(fp)
        if not fp.startswith(pf_manager.base_folder):
            return '', 404

        if os.path.exists(fp):
            return send_file(fp)
        else:
            return '', 404

    @app.route('/api/post', methods=['GET'])
    @require_auth
    def list_posts():
        articles = [a.model_dump(mode='json') for a in pf_manager.list_articles()]
        return jsonify({'items': articles})

    @app.route('/api/post/<path:post_name>', methods=['GET'])
    @require_auth
    def get_post(post_name):
        article = pf_manager.extract_article(post_name)
        if article is None:
            return '', 404
        return article

    install_to_flask(frontend_assets, app)

    return app


if __name__ == '__main__':  # pragma: no cover
    _frontend_assets = {
        'index.html': "dataset.sh web ui is disabled"
    }

    if not DISABLE_UI:
        _frontend_assets = load_frontend_assets()

    app = create_app(frontend_assets=_frontend_assets)
