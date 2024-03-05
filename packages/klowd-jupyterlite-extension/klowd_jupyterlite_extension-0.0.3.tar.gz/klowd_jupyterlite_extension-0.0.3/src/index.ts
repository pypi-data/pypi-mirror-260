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

export const copyShareableLinkId = 'klowd-jupyterlite-extension:share-link';

/**
 * Initialization data for the klowd-jupyterlite-extension extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'klowd-jupyterlite-extension:plugin',
  description: 'A JupyterLab KLOWD extension.',
  autoStart: true,
  optional: [ISettingRegistry, IThemeManager, IFileBrowserFactory],
  activate: (
    app: JupyterFrontEnd,
    settingRegistry: ISettingRegistry | null,
    themeManager: IThemeManager,
    factory: IFileBrowserFactory,
  ) => {
    console.log('JupyterLab extension klowd-jupyterlite-extension is activated!');
    const { commands } = app;
    const { tracker } = factory;

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
          console.log('klowd-jupyterlite-extension settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for klowd-jupyterlite-extension.', reason);
        });
    }

    /* Incoming messages management */
    window.addEventListener('message', event => {
      if (event.data.type === 'switch theme') {
        console.log('Plugin message received:', event.data);

        themeManager.setTheme(
          themeManager.theme === 'JupyterLab Dark'
            ? 'JupyterLab Light'
            : 'JupyterLab Dark'
        );
      }
    });

    /* Outgoing messages management */
    const notifyThemeChanged = (): void => {
      const message = {
        type: 'theme switched',
        theme: themeManager.theme
      };
      window.parent.postMessage(message, '*');
      console.log('Message sent to the host:', message);
    };
    themeManager.themeChanged.connect(notifyThemeChanged);
  }
};

export default plugin;
