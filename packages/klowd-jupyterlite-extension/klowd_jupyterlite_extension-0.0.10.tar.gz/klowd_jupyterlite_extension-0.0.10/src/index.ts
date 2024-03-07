import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { Clipboard, IThemeManager } from '@jupyterlab/apputils';
import { PageConfig } from '@jupyterlab/coreutils';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { linkIcon } from '@jupyterlab/ui-components';
import { filter } from '@lumino/algorithm';

export const copyShareableLinkId = 'klowd_jupyterlite_extension:klowd-share-link';

const DARK_THEME_NAME = 'JupyterLab Dark';
const LIGHT_THEME_NAME = 'JupyterLab Light';

/**
 * Initialization data for the klowd_jupyterlite_extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'klowd_jupyterlite_extension:plugin',
  description: 'A JupyterLab KLOWD extension.',
  autoStart: true,
  optional: [ISettingRegistry, IThemeManager, IFileBrowserFactory],
  activate: (
    app: JupyterFrontEnd,
    settingRegistry: ISettingRegistry | null,
    themeManager: IThemeManager,
    factory: IFileBrowserFactory,
  ) => {
    console.log('JupyterLab extension klowd_jupyterlite_extension is activated!');
    const { commands } = app;
    const { tracker } = factory;
    let token = 'test token';

    // https://github.com/jupyterlite/jupyterlite/blob/c865a593745ef4f8227e41b51043af5317f0e803/packages/application-extension/src/index.tsx#L63
    commands.addCommand(copyShareableLinkId, {
      execute: () => {
        const widget = tracker.currentWidget;
        if (!widget) {
          return;
        }

        const shareUrl = PageConfig.getShareUrl();
        const models = Array.from(
          filter(widget.selectedItems(), (item) => item.type !== 'directory'),
        );

        if (!models.length) {
          return;
        }

        const url = new URL(shareUrl);
        models.forEach((model) => {
          url.searchParams.append('file', model.path);
        });
        Clipboard.copyToSystem(url.href);
      },
      isVisible: () =>
        !!tracker.currentWidget &&
        Array.from(tracker.currentWidget.selectedItems()).length >= 1,
      icon: linkIcon.bindprops({ stylesheet: 'menuItem' }),
      label: 'Копировать ссылку на файл',
    });

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('klowd_jupyterlite_extension settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for klowd_jupyterlite_extension.', reason);
        });
    }

    /* Incoming messages management */
    window.addEventListener('message', event => {
      if (event.data.type === 'theme') {
        console.log('Plugin message received:', event.data);

        themeManager.setTheme(
          event.data.payload === 'light'
            ? LIGHT_THEME_NAME
            : DARK_THEME_NAME
        );
      }

      if (event.data.type === 'token') {
        (window as any).kloud_token = event.data.payload;
      }
    });

    /* Outgoing messages management */
    const notifyThemeChanged = (): void => {
      const message = {
        type: 'theme',
        payload: themeManager.theme === DARK_THEME_NAME ? 'dark' : 'light'
      };
      window.parent.postMessage(message, '*');
      console.log('Message sent to the host:', message);
    };
    themeManager.themeChanged.connect(notifyThemeChanged);

    window.fetch = (function (origFetch) {
      return function myFetch(resource, options = {}) {
          console.log('fetch intercepted for', resource);
          const headers = new Headers(options.headers);
          headers.append('Authorization', `Bearer ${token}`);

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
