import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the kloudplugin extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'kloudplugin:plugin',
  description: 'A JupyterLab KLOUD extension.',
  autoStart: true,
  optional: [ISettingRegistry, IThemeManager],
  activate: (
    app: JupyterFrontEnd,
    settingRegistry: ISettingRegistry | null,
    themeManager: IThemeManager
  ) => {
    console.log('JupyterLab extension kloudplugin is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('kloudplugin settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for kloudplugin.', reason);
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
