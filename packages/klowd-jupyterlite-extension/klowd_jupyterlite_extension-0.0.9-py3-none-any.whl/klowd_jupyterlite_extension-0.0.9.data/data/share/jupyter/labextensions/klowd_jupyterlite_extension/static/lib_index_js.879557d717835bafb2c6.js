"use strict";
(self["webpackChunkklowd_jupyterlite_extension"] = self["webpackChunkklowd_jupyterlite_extension"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   copyShareableLinkId: () => (/* binding */ copyShareableLinkId),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__);






const copyShareableLinkId = 'klowd_jupyterlite_extension:klowd-share-link';
const DARK_THEME_NAME = 'JupyterLab Dark';
const LIGHT_THEME_NAME = 'JupyterLab Light';
/**
 * Initialization data for the klowd_jupyterlite_extension extension.
 */
const plugin = {
    id: 'klowd_jupyterlite_extension:plugin',
    description: 'A JupyterLab KLOWD extension.',
    autoStart: true,
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_3__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager, _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_2__.IFileBrowserFactory],
    activate: (app, settingRegistry, themeManager, factory) => {
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
                const shareUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PageConfig.getShareUrl();
                const models = Array.from((0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_5__.filter)(widget.selectedItems(), (item) => item.type !== 'directory'));
                if (!models.length) {
                    return;
                }
                const url = new URL(shareUrl);
                models.forEach((model) => {
                    url.searchParams.append('file', model.path);
                });
                _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Clipboard.copyToSystem(url.href);
            },
            isVisible: () => !!tracker.currentWidget &&
                Array.from(tracker.currentWidget.selectedItems()).length >= 1,
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.linkIcon.bindprops({ stylesheet: 'menuItem' }),
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
                themeManager.setTheme(event.data.payload === 'light'
                    ? LIGHT_THEME_NAME
                    : DARK_THEME_NAME);
            }
            if (event.data.type === 'token') {
                token = event.data.payload;
            }
        });
        /* Outgoing messages management */
        const notifyThemeChanged = () => {
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
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.879557d717835bafb2c6.js.map