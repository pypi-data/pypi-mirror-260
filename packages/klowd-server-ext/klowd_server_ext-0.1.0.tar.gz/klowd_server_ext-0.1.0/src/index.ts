import {
  JupyterLiteServer,
  JupyterLiteServerPlugin
} from '@jupyterlite/server';

/**
 * Initialization data for the klowd_server_ext extension.
 */
const plugin: JupyterLiteServerPlugin<void> = {
  id: 'klowd_server_ext:plugin',
  autoStart: true,
  activate: (app: JupyterLiteServer) => {
    console.log('JupyterLite server extension klowd_server_ext is activated!');

    window.fetch = (function (origFetch) {
      return function myFetch(resource: any, options = {}) {
          console.log('fetch intercepted for', resource);
          const headers = new Headers((options as any).headers);
          headers.append('Authorization', `Bearer MYTOKEN`);

          const modifiedOptions = {
            ...options,
            headers: headers,
          };

          return origFetch(resource, modifiedOptions);
      };
    })(window.fetch);
  }
};

export default plugin;
