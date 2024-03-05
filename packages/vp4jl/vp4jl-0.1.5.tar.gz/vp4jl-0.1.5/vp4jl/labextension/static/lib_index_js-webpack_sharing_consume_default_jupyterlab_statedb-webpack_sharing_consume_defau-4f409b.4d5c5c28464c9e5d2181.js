"use strict";
(self["webpackChunkvp4jl"] = self["webpackChunkvp4jl"] || []).push([["lib_index_js-webpack_sharing_consume_default_jupyterlab_statedb-webpack_sharing_consume_defau-4f409b"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");
/* harmony import */ var _namepace__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./namepace */ "./lib/namepace.js");
/* harmony import */ var _request__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! ./request */ "./lib/request.js");
/* harmony import */ var _node_extension__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./node-extension */ "./lib/node-extension.js");
/* harmony import */ var _model_factory__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ./model-factory */ "./lib/model-factory.js");
/* harmony import */ var _widget_factory__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./widget-factory */ "./lib/widget-factory.js");
/* harmony import */ var _toolbar_factory__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./toolbar-factory */ "./lib/toolbar-factory.js");
/* harmony import */ var _tracker__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./tracker */ "./lib/tracker.js");
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! vprcs */ "webpack/sharing/consume/default/vprcs/vprcs");
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(vprcs__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _visual_code_cell__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./visual-code-cell */ "./lib/visual-code-cell/index.js");

















const vp4jl = {
    id: 'vp4jl:plugin',
    autoStart: true,
    requires: [_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_5__.IRenderMimeRegistry],
    provides: _tracker__WEBPACK_IMPORTED_MODULE_8__.IVPTrackerToken,
    activate: activateVp4jl
};
const vp4jlCommands = {
    id: 'vp4jl:Commands',
    autoStart: true,
    requires: [
        _jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell,
        _tracker__WEBPACK_IMPORTED_MODULE_8__.IVPTrackerToken,
        _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_6__.ISessionContextDialogs,
        _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IFileBrowserFactory,
        _node_extension__WEBPACK_IMPORTED_MODULE_9__.NodeExtensionToken
    ],
    optional: [_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_1__.IDefaultFileBrowser],
    activate: activateVp4jlCommands
};
const vp4jlAttachCommandsToGui = {
    id: 'vp4jl:AttachCommandsToGui',
    autoStart: true,
    requires: [_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_3__.IMainMenu, _tracker__WEBPACK_IMPORTED_MODULE_8__.IVPTrackerToken],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_2__.ILauncher, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_6__.ICommandPalette],
    activate: activateVp4jlAttachCommandsToGui
};
const vp4jlRestorer = {
    id: 'vp4jl:Restorer',
    autoStart: true,
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer, _tracker__WEBPACK_IMPORTED_MODULE_8__.IVPTrackerToken],
    activate: activateVp4jlRestorer
};
const vp4jlNodeExtension = {
    id: 'vp4jl:NodeExtension',
    autoStart: true,
    optional: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILayoutRestorer],
    provides: _node_extension__WEBPACK_IMPORTED_MODULE_9__.NodeExtensionToken,
    activate: activateVp4jlNodeExtension
};
const vp4jlFixContextMenuClose = {
    id: 'vp4jl:FixContextMenuClose',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_0__.ILabShell],
    activate: activateVp4jlFixContextMenuClose
};
const plugins = [
    vp4jl,
    vp4jlCommands,
    vp4jlAttachCommandsToGui,
    vp4jlRestorer,
    vp4jlNodeExtension,
    vp4jlFixContextMenuClose,
    ..._visual_code_cell__WEBPACK_IMPORTED_MODULE_10__["default"]
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);
function activateVp4jl(app, rendermime) {
    const vp4jlIDs = _namepace__WEBPACK_IMPORTED_MODULE_11__.vp4jlIDs;
    const tracker = new _tracker__WEBPACK_IMPORTED_MODULE_8__.VPTracker({
        namespace: vp4jlIDs.trackerNamespace
    });
    const widgetFactory = new _widget_factory__WEBPACK_IMPORTED_MODULE_12__.VPWidgetFactory({
        name: vp4jlIDs.widgetFactory,
        modelName: vp4jlIDs.modelFactory,
        fileTypes: [vp4jlIDs.fileType],
        defaultFor: [vp4jlIDs.fileType],
        toolbarFactory: (0,_toolbar_factory__WEBPACK_IMPORTED_MODULE_13__.getToolbarFactory)(app.commands, vp4jlIDs.widgetFactory)
    }, rendermime);
    widgetFactory.widgetCreated.connect((sender, widget) => {
        widget.context.pathChanged.connect(() => {
            tracker.save(widget);
        });
        tracker.add(widget);
    });
    app.docRegistry.addWidgetFactory(widgetFactory);
    app.docRegistry.addModelFactory(new _model_factory__WEBPACK_IMPORTED_MODULE_14__.VPModelFactory());
    app.docRegistry.addFileType({
        name: vp4jlIDs.fileType,
        displayName: 'VP File',
        mimeTypes: ['text/json', 'application/json'],
        extensions: [vp4jlIDs.fileExtension],
        fileFormat: 'text',
        contentType: 'file'
    });
    return tracker;
}
function activateVp4jlCommands(app, labShell, tracker, sessionDialogs, browserFactory, nodeExtension, defaultFileBrowser) {
    const vp4jlIDs = _namepace__WEBPACK_IMPORTED_MODULE_11__.vp4jlIDs;
    const cmdIds = _namepace__WEBPACK_IMPORTED_MODULE_11__.vp4jlCommandIDs;
    const { shell } = app;
    const isEnabled = () => {
        return isFocusVPWidget(shell, tracker);
    };
    const isEnabledDependOnSelected = (args) => {
        var _a;
        if (!isEnabled()) {
            return false;
        }
        const current = getCurrent(tracker, shell, { ...args, activate: false });
        return !!((_a = current === null || current === void 0 ? void 0 : current.model.vpActions) === null || _a === void 0 ? void 0 : _a.getSelectedCounts().nodesCount);
    };
    app.commands.addCommand(cmdIds.createNew, {
        label: args => args['isPalette']
            ? vp4jlIDs.createNewLabelInPalette
            : args['isContextMenu']
                ? vp4jlIDs.createNewLabelInContextMenu
                : vp4jlIDs.createNewLabelInFileMenu,
        caption: vp4jlIDs.caption,
        execute: async (args) => {
            var _a;
            const cwd = args['cwd'] ||
                ((_a = browserFactory.tracker.currentWidget) === null || _a === void 0 ? void 0 : _a.model.path) ||
                (defaultFileBrowser === null || defaultFileBrowser === void 0 ? void 0 : defaultFileBrowser.model.path) ||
                '';
            const model = await app.commands.execute('docmanager:new-untitled', {
                path: cwd,
                contentType: 'file',
                fileFormat: 'text',
                ext: vp4jlIDs.fileExtension,
                type: 'file'
            });
            if (model !== undefined) {
                const widget = (await app.commands.execute('docmanager:open', {
                    path: model.path,
                    factory: vp4jlIDs.widgetFactory
                }));
                widget.isUntitled = true;
                return widget;
            }
        }
    });
    app.commands.addCommand(cmdIds.run, {
        label: 'Run Visual Programming File',
        caption: 'Run the visual programming file',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            current === null || current === void 0 ? void 0 : current.execute();
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.runIcon : undefined),
        isEnabled
    });
    app.commands.addCommand(cmdIds.copy, {
        label: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return !args.toolbar
                ? 'Copy'
                : !((_a = current === null || current === void 0 ? void 0 : current.model.vpActions) === null || _a === void 0 ? void 0 : _a.getSelectedCounts().nodesCount)
                    ? 'Copy Node'
                    : 'Copy Nodes';
        },
        caption: args => {
            var _a;
            const current = getCurrent(tracker, shell, { ...args, activate: false });
            return !((_a = current === null || current === void 0 ? void 0 : current.model.vpActions) === null || _a === void 0 ? void 0 : _a.getSelectedCounts().nodesCount)
                ? 'Copy this node'
                : 'Copy theses nodes';
        },
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                (_a = current.model.vpActions) === null || _a === void 0 ? void 0 : _a.copySelectedNodeToClipboard();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.copyIcon : undefined),
        isEnabled: args => {
            return isEnabledDependOnSelected(args);
        }
    });
    app.commands.addCommand(cmdIds.paste, {
        label: 'Paste',
        caption: 'Paste from the clipboard',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                (_a = current.model.vpActions) === null || _a === void 0 ? void 0 : _a.pasteFromClipboard();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.pasteIcon : undefined),
        isEnabled: args => {
            return isEnabledDependOnSelected(args);
        }
    });
    app.commands.addCommand(cmdIds.del, {
        label: 'Delete',
        caption: 'Delete the selected node',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                (_a = current.model.vpActions) === null || _a === void 0 ? void 0 : _a.deleteSelectedElements();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.deleteIcon : undefined),
        isEnabled: args => {
            return isEnabledDependOnSelected(args);
        }
    });
    app.commands.addCommand(cmdIds.cut, {
        label: 'Cut',
        caption: 'Cut the selected node',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                (_a = current.model.vpActions) === null || _a === void 0 ? void 0 : _a.cutSelectedNodesToClipboard();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.cutIcon : undefined),
        isEnabled: args => {
            return isEnabledDependOnSelected(args);
        }
    });
    app.commands.addCommand(cmdIds.duplicate, {
        label: 'Duplicate',
        caption: 'Duplicate the selected node',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                (_a = current.model.vpActions) === null || _a === void 0 ? void 0 : _a.duplicateSelectedNodes();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.duplicateIcon : undefined),
        isEnabled: args => {
            return isEnabledDependOnSelected(args);
        }
    });
    app.commands.addCommand(cmdIds.deleteAll, {
        label: 'Delete All',
        caption: 'Delete all nodes and edges',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (current) {
                (_a = current.model.vpActions) === null || _a === void 0 ? void 0 : _a.clear();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.clearIcon : undefined),
        isEnabled
    });
    app.commands.addCommand(cmdIds.interruptKernel, {
        label: 'Interrupt Kernel',
        caption: 'Interrupt the kernel',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.interrupt();
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.stopIcon : undefined),
        isEnabled
    });
    app.commands.addCommand(cmdIds.restartKernel, {
        label: 'Restart Kernel',
        caption: 'Restart the kernel',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.restart(current.sessionContext);
            }
        },
        icon: args => (args.toolbar ? _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.refreshIcon : undefined),
        isEnabled
    });
    app.commands.addCommand(cmdIds.clearOutput, {
        label: 'Clear Output',
        caption: 'Clear the output',
        execute: args => {
            console.log('clear output');
        },
        isEnabled
    });
    app.commands.addCommand(cmdIds.reconnectKernel, {
        label: 'Reconnect to Kernel',
        caption: 'Reconnect to the kernel',
        execute: args => {
            var _a;
            const current = getCurrent(tracker, shell, args);
            if (!current) {
                return;
            }
            const kernel = (_a = current.context.sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
            if (kernel) {
                return kernel.reconnect();
            }
        },
        isEnabled
    });
    app.commands.addCommand(cmdIds.restartKernelAndRun, {
        label: 'Restart Kernel and Run',
        caption: 'Restart the kernel and re-run the whole file',
        execute: async (args) => {
            const restarted = await app.commands.execute(cmdIds.restartKernel, {
                activate: false
            });
            if (restarted) {
                await app.commands.execute(cmdIds.run);
            }
        },
        icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.fastForwardIcon,
        isEnabled
    });
    app.commands.addCommand(cmdIds.shutdownKernel, {
        label: 'Shut Down Kernel',
        caption: 'Shutdown the kernel',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return current.context.sessionContext.shutdown();
            }
        },
        isEnabled
    });
    app.commands.addCommand(cmdIds.changeKernel, {
        label: 'Change Kernel…',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                return sessionDialogs.selectKernel(current.context.sessionContext);
            }
        },
        isEnabled
    });
    app.commands.addCommand(cmdIds.showNodeExtension, {
        label: 'Show Node Packages Manager',
        execute: () => {
            labShell.activateById(vp4jlIDs.nodeExtension);
        }
    });
    app.commands.addCommand(cmdIds.hideNodeExtension, {
        label: 'Hide Node Extension',
        execute: () => {
            labShell.collapseLeft();
        }
    });
    app.commands.addCommand(cmdIds.toggleNodeExtension, {
        label: 'Node Packages Manager',
        execute: () => {
            if (nodeExtension.isHidden) {
                return app.commands.execute(cmdIds.showNodeExtension, void 0);
            }
            return app.commands.execute(cmdIds.hideNodeExtension, void 0);
        }
    });
    app.commands.addCommand(cmdIds.toggleOutput, {
        label: 'Output Area',
        execute: args => {
            const current = getCurrent(tracker, shell, args);
            if (current) {
                current.toggleOutput();
            }
        },
        isEnabled
    });
}
function isFocusVPWidget(shell, tracker) {
    return (tracker.currentWidget !== null &&
        tracker.currentWidget === shell.currentWidget);
}
function getCurrent(tracker, shell, args) {
    const widget = tracker.currentWidget;
    const activate = args['activate'] !== false;
    if (activate && widget) {
        shell.activateById(widget.id);
    }
    return widget;
}
function activateVp4jlAttachCommandsToGui(app, mainMenu, tracker, launcher, palette) {
    const cmdIds = _namepace__WEBPACK_IMPORTED_MODULE_11__.vp4jlCommandIDs;
    const isEnabled = () => {
        return isFocusVPWidget(app.shell, tracker);
    };
    mainMenu.fileMenu.newMenu.addItem({ command: cmdIds.createNew, rank: 30 });
    mainMenu.editMenu.addGroup([
        { command: cmdIds.copy },
        { command: cmdIds.paste },
        { command: cmdIds.duplicate },
        { command: cmdIds.cut },
        { command: cmdIds.del },
        { command: cmdIds.deleteAll }
    ], 4);
    mainMenu.runMenu.codeRunners.run.add({
        id: cmdIds.run,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.interruptKernel.add({
        id: cmdIds.interruptKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.restartKernel.add({
        id: cmdIds.restartKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.reconnectToKernel.add({
        id: cmdIds.reconnectKernel,
        isEnabled
    });
    mainMenu.runMenu.codeRunners.restart.add({
        id: cmdIds.restartKernelAndRun,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.shutdownKernel.add({
        id: cmdIds.shutdownKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.changeKernel.add({
        id: cmdIds.changeKernel,
        isEnabled
    });
    mainMenu.kernelMenu.kernelUsers.clearWidget.add({
        id: cmdIds.clearOutput,
        isEnabled
    });
    mainMenu.editMenu.clearers.clearCurrent.add({
        id: cmdIds.clearOutput,
        isEnabled
    });
    mainMenu.viewMenu.addItem({
        command: cmdIds.toggleNodeExtension,
        rank: 9
    });
    mainMenu.viewMenu.addItem({
        command: cmdIds.toggleOutput,
        rank: 9
    });
    launcher === null || launcher === void 0 ? void 0 : launcher.add({
        command: cmdIds.createNew,
        category: cmdIds.commandCategory,
        rank: 0
    });
    palette === null || palette === void 0 ? void 0 : palette.addItem({
        command: cmdIds.createNew,
        category: cmdIds.commandCategory,
        args: { isPalette: true }
    });
    app.contextMenu.addItem({
        command: cmdIds.createNew,
        selector: '.jp-DirListing-content',
        rank: 53,
        args: {
            isContextMenu: true
        }
    });
}
function activateVp4jlRestorer(app, restorer, tracker) {
    const vp4jlIDs = _namepace__WEBPACK_IMPORTED_MODULE_11__.vp4jlIDs;
    if (restorer && tracker) {
        restorer.restore(tracker, {
            command: 'docmanager:open',
            args: widget => ({
                path: widget.context.path,
                factory: vp4jlIDs.widgetFactory
            }),
            name: widget => widget.context.path
        });
    }
}
function activateVp4jlNodeExtension(app, restorer) {
    const nodeExtension = new _node_extension__WEBPACK_IMPORTED_MODULE_9__.NodeExtension();
    app.shell.add(nodeExtension, 'left');
    if (restorer) {
        restorer.add(nodeExtension, 'vp4jlNodeExtension');
    }
    fetchNodeExtensions();
    return nodeExtension;
}
function fetchNodeExtensions() {
    (0,_request__WEBPACK_IMPORTED_MODULE_15__.requestAPI)('node_extension_manager')
        .then(data => {
        Object.entries(data.packages).forEach(([key, value]) => {
            // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
            (0,vprcs__WEBPACK_IMPORTED_MODULE_7__.LoadPackageToRegistry)(key, value);
        });
    })
        .catch(reason => {
        console.error(`The vp4jl server error:\n${reason}`);
        console.error(`The vp4jl server error:\n${reason}`);
    });
}
function activateVp4jlFixContextMenuClose(app, labShell) {
    // close the context menu when switch the tab
    labShell.currentChanged.connect((_, args) => {
        if (args.oldValue instanceof _widget__WEBPACK_IMPORTED_MODULE_16__.VPWidget) {
            args.oldValue.content.deactivate();
        }
        closeDefaultContextMenu();
    });
    function closeDefaultContextMenu() {
        if (app.contextMenu.menu.isAttached) {
            app.contextMenu.menu.close();
        }
    }
    // close the context menu when click the tab
    function addClickEventToSideBar() {
        const sideBars = document.getElementsByClassName('jp-SideBar');
        if (!sideBars.length) {
            window.requestAnimationFrame(() => {
                addClickEventToSideBar();
            });
            return;
        }
        for (const sideBar of sideBars) {
            for (const tab of sideBar.getElementsByClassName('lm-TabBar-tab')) {
                tab.addEventListener('click', closeDefaultContextMenu);
            }
        }
    }
    window.requestAnimationFrame(() => {
        addClickEventToSideBar();
    });
}


/***/ }),

/***/ "./lib/model-factory.js":
/*!******************************!*\
  !*** ./lib/model-factory.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VPModelFactory: () => (/* binding */ VPModelFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./model */ "./lib/model.js");
/* harmony import */ var _namepace__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./namepace */ "./lib/namepace.js");



class VPModelFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.TextModelFactory {
    get name() {
        return _namepace__WEBPACK_IMPORTED_MODULE_1__.vp4jlIDs.modelFactory;
    }
    createNew(options = {}) {
        const collaborative = options.collaborationEnabled && this.collaborative;
        return new _model__WEBPACK_IMPORTED_MODULE_2__.VPModel({
            ...options,
            collaborationEnabled: collaborative
        });
    }
}


/***/ }),

/***/ "./lib/model.js":
/*!**********************!*\
  !*** ./lib/model.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VPModel: () => (/* binding */ VPModel)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./utils */ "./lib/utils.js");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__);




class VPModel extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentModel {
    constructor(options) {
        super(options);
        this._kernelSpec = {};
        this._vpContent = null;
        this._kernelSpecChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._vpContentChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._vpActions = null;
        this._toolbarItems = {};
        this._rendermime = null;
        this._outputAreaModel = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputAreaModel();
        this._outputAreaModelChanged = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this.contentChanged.connect(this._setProperties.bind(this));
    }
    _setProperties() {
        var _a;
        const model = JSON.parse(this.toString());
        if (model.output &&
            !(0,_utils__WEBPACK_IMPORTED_MODULE_3__.isSameContent)(this._outputAreaModel.toJSON(), model.output)) {
            this._outputAreaModel.fromJSON((_a = model.output) !== null && _a !== void 0 ? _a : []);
            this._outputAreaModelChanged.emit();
        }
        this.kernelSpec = model.kernelSpec;
        this.vpContent = model.vpContent;
    }
    _setModelContent() {
        var _a;
        const content = JSON.stringify({
            vpContent: this.vpContent,
            kernelSpec: this.kernelSpec,
            output: (_a = this._outputAreaModel) === null || _a === void 0 ? void 0 : _a.toJSON()
        });
        if (this.toString() !== content) {
            this.fromString(content);
        }
    }
    saveOutputModel() {
        var _a;
        const content = JSON.stringify({
            vpContent: this.vpContent,
            kernelSpec: this.kernelSpec,
            output: (_a = this._outputAreaModel) === null || _a === void 0 ? void 0 : _a.toJSON()
        });
        if (this.toString() !== content) {
            this.fromString(content);
        }
    }
    async setKernelSpec(kernel) {
        if (!kernel) {
            return;
        }
        const spec = await kernel.spec;
        if (this.isDisposed) {
            return;
        }
        const newSpec = {
            name: kernel.name,
            display_name: spec === null || spec === void 0 ? void 0 : spec.display_name,
            language: spec === null || spec === void 0 ? void 0 : spec.language
        };
        if (!(0,_utils__WEBPACK_IMPORTED_MODULE_3__.isSameContent)(this.kernelSpec, newSpec)) {
            this.kernelSpec = newSpec;
        }
    }
    set kernelSpec(kernelSpec) {
        if (!(0,_utils__WEBPACK_IMPORTED_MODULE_3__.isSameContent)(this.kernelSpec, kernelSpec !== null && kernelSpec !== void 0 ? kernelSpec : {})) {
            this._kernelSpec = kernelSpec;
            this._kernelSpecChanged.emit(this._kernelSpec);
            this._setModelContent();
        }
    }
    get kernelSpec() {
        return this._kernelSpec;
    }
    setVpContent(vpContent) {
        this.vpContent =
            typeof vpContent === 'string'
                ? JSON.parse(vpContent === '' ? 'null' : vpContent)
                : vpContent;
    }
    set vpContent(vpContent) {
        if (!(0,_utils__WEBPACK_IMPORTED_MODULE_3__.isSameContent)(this._vpContent, vpContent)) {
            this._vpContent = vpContent;
            this._setModelContent();
        }
    }
    get vpContent() {
        return this._vpContent;
    }
    get outputAreaModel() {
        return this._outputAreaModel;
    }
    get kernelSpecChanged() {
        return this._kernelSpecChanged;
    }
    get vpContentChanged() {
        return this._vpContentChanged;
    }
    get vpActions() {
        return this._vpActions;
    }
    setVpActions(vpActions) {
        this._vpActions = vpActions;
    }
    get toolbarItems() {
        return this._toolbarItems;
    }
    setToolbarItems(toolbarItems) {
        toolbarItems === null || toolbarItems === void 0 ? void 0 : toolbarItems.forEach(item => {
            this._toolbarItems[item.name] = item;
        });
    }
    get rendermime() {
        return this._rendermime;
    }
    setRendermime(rendermime) {
        this._rendermime = rendermime;
    }
    get outputAreaModelChanged() {
        return this._outputAreaModelChanged;
    }
}


/***/ }),

/***/ "./lib/namepace.js":
/*!*************************!*\
  !*** ./lib/namepace.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   vp4jlCommandIDs: () => (/* binding */ vp4jlCommandIDs),
/* harmony export */   vp4jlIDs: () => (/* binding */ vp4jlIDs)
/* harmony export */ });
var vp4jlIDs;
(function (vp4jlIDs) {
    vp4jlIDs.fileExtension = '.vp4jl';
    vp4jlIDs.fileType = 'vp4jl';
    vp4jlIDs.trackerNamespace = 'vp4jl';
    vp4jlIDs.widgetFactory = 'vp4jl widget factory';
    vp4jlIDs.modelFactory = 'vp4jl model factory';
    vp4jlIDs.createNewLabelInPalette = 'New Visual Programming File';
    vp4jlIDs.createNewLabelInFileMenu = 'Visual Programming File';
    vp4jlIDs.createNewLabelInContextMenu = 'Visual Programming File';
    vp4jlIDs.caption = 'Create a new Visual Programming file';
    vp4jlIDs.nodeExtension = 'vp4jl-node-extension';
})(vp4jlIDs || (vp4jlIDs = {}));
var vp4jlCommandIDs;
(function (vp4jlCommandIDs) {
    vp4jlCommandIDs.commandCategory = 'Visual Programming';
    vp4jlCommandIDs.createNew = 'vp4jl:create-new';
    vp4jlCommandIDs.run = 'vp4jl:run';
    vp4jlCommandIDs.copy = 'vp4jl:copy';
    vp4jlCommandIDs.paste = 'vp4jl:paste';
    vp4jlCommandIDs.del = 'vp4jl:delete';
    vp4jlCommandIDs.cut = 'vp4jl:cut';
    vp4jlCommandIDs.duplicate = 'vp4jl:duplicate';
    vp4jlCommandIDs.deleteAll = 'vp4jl:clear';
    vp4jlCommandIDs.clearOutput = 'vp4jl:clear-output';
    vp4jlCommandIDs.shutdownKernel = 'vp4jl:shutdown-kernel';
    vp4jlCommandIDs.interruptKernel = 'vp4jl:interrupt-kernel';
    vp4jlCommandIDs.restartKernel = 'vp4jl:restart-kernel';
    vp4jlCommandIDs.reconnectKernel = 'vp4jl:reconnect-kernel';
    vp4jlCommandIDs.changeKernel = 'vp4jl:change-kernel';
    vp4jlCommandIDs.restartKernelAndRun = 'vp4jl:restart-kernel-and-run';
    vp4jlCommandIDs.showNodeExtension = 'vp4jl:show-node-extension';
    vp4jlCommandIDs.hideNodeExtension = 'vp4jl:hide-node-extension';
    vp4jlCommandIDs.toggleNodeExtension = 'vp4jl:toggle-node-extension';
    vp4jlCommandIDs.toggleOutput = 'vp4jl:toggle-output';
})(vp4jlCommandIDs || (vp4jlCommandIDs = {}));


/***/ }),

/***/ "./lib/node-extension.js":
/*!*******************************!*\
  !*** ./lib/node-extension.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   NodeExtension: () => (/* binding */ NodeExtension),
/* harmony export */   NodeExtensionToken: () => (/* binding */ NodeExtensionToken)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! vprcs */ "webpack/sharing/consume/default/vprcs/vprcs");
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(vprcs__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _namepace__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./namepace */ "./lib/namepace.js");
/* harmony import */ var _request__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./request */ "./lib/request.js");
/* harmony import */ var _request_token__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./request-token */ "./lib/request-token.js");










function NodeExtensionWidget({ fetching, onInstallNodeExtension, uninstallNodeExtension, enableNodeExtension, url }) {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(vprcs__WEBPACK_IMPORTED_MODULE_6__.Progress, { enable: fetching }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(vprcs__WEBPACK_IMPORTED_MODULE_6__.NodeLibraryList, { title: "INSTALLED", nodeExtensions: { ...vprcs__WEBPACK_IMPORTED_MODULE_6__.nodeConfigRegistry.getAllNodeConfigs() }, onInstall: onInstallNodeExtension, onUninstall: (name) => {
                uninstallNodeExtension(name);
            }, onDisable: (name) => {
                enableNodeExtension(name, false);
            }, onEnable: (name) => {
                enableNodeExtension(name, true);
            }, url: url, tokens: (0,_request_token__WEBPACK_IMPORTED_MODULE_7__.requestToken)() })));
}
class NodeExtension extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_5__.ReactWidget {
    constructor() {
        super();
        this.fetching = false;
        this.settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_3__.ServerConnection.makeSettings();
        this.requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_2__.URLExt.join(this.settings.baseUrl, 'vp4jl', // API Namespace
        'node_extension_manager');
        this.id = _namepace__WEBPACK_IMPORTED_MODULE_8__.vp4jlIDs.nodeExtension;
        this.node.style.background = 'var(--jp-layout-color1)';
        this.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.extensionIcon;
        this.title.caption = 'Node Extension Manager';
        this.addClass('jp-NodeExtension');
        this.addClass('lm-StackedPanel-child');
        this.addClass('p-StackedPanel-child');
    }
    installNodeExtension(data) {
        console.log(data);
        const obj = JSON.parse(data);
        for (const name in obj.packages) {
            (0,vprcs__WEBPACK_IMPORTED_MODULE_6__.LoadPackageToRegistry)(name, obj.packages[name]);
        }
        this.update();
        console.log(vprcs__WEBPACK_IMPORTED_MODULE_6__.imageTypeConversionGraph);
    }
    uninstallNodeExtension(name) {
        this.fetching = true;
        this.update();
        (0,_request__WEBPACK_IMPORTED_MODULE_9__.requestAPI)('node_extension_manager', {
            method: 'DELETE',
            body: JSON.stringify(name)
        })
            .then(data => {
            if (data.status === 'ok') {
                vprcs__WEBPACK_IMPORTED_MODULE_6__.nodeConfigRegistry.removeNodeConfig(name);
                this.update();
            }
        })
            .catch(reason => {
            console.error(`The node extension manager appears to be missing.\n${reason}`);
        })
            .finally(() => {
            this.fetching = false;
            this.update();
        });
    }
    enableNodeExtension(name, enable) {
        this.fetching = true;
        this.update();
        (0,_request__WEBPACK_IMPORTED_MODULE_9__.requestAPI)('node_extension_manager', {
            method: 'POST',
            body: JSON.stringify({ name: name, enable: enable })
        })
            .then(data => {
            if (data.status === 'ok') {
                vprcs__WEBPACK_IMPORTED_MODULE_6__.nodeConfigRegistry.enableNodeConfig(name, enable);
                this.update();
            }
        })
            .catch(reason => {
            console.error(`The node extension manager appears to be missing.\n${reason}`);
        })
            .finally(() => {
            this.fetching = false;
            this.update();
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(NodeExtensionWidget, { fetching: this.fetching, onInstallNodeExtension: this.installNodeExtension.bind(this), uninstallNodeExtension: this.uninstallNodeExtension.bind(this), enableNodeExtension: this.enableNodeExtension.bind(this), url: this.requestUrl }));
    }
}
const NodeExtensionToken = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('@jupyterlab/vp4jl:INodeExtension', `A node package extension panel for visual programming files.
  This is used to install, uninstall, enable or disable node packages that can be used in the visual programming files.`);


/***/ }),

/***/ "./lib/request-token.js":
/*!******************************!*\
  !*** ./lib/request-token.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestToken: () => (/* binding */ requestToken)
/* harmony export */ });
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__);

function getCookie(name) {
    // From http://www.tornadoweb.org/en/stable/guide/security.html
    const matches = document.cookie.match('\\b' + name + '=([^;]*)\\b');
    return matches === null || matches === void 0 ? void 0 : matches[1];
}
function requestToken() {
    const token = {
        authenticated: false,
        Authorization: null,
        'X-XSRFToken': null
    };
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_0__.ServerConnection.makeSettings();
    if (settings.token) {
        token.authenticated = true;
        token['Authorization'] = `token ${settings.token}`;
    }
    if (typeof document !== 'undefined' && (document === null || document === void 0 ? void 0 : document.cookie)) {
        const xsrfToken = getCookie('_xsrf');
        if (xsrfToken !== undefined) {
            token.authenticated = true;
            token['X-XSRFToken'] = xsrfToken;
        }
    }
    return token;
}


/***/ }),

/***/ "./lib/request.js":
/*!************************!*\
  !*** ./lib/request.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   requestAPI: () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'vp4jl', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/toolbar-factory.js":
/*!********************************!*\
  !*** ./lib/toolbar-factory.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   getToolbarFactory: () => (/* binding */ getToolbarFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils_lib_toolbar__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/apputils/lib/toolbar */ "./node_modules/@jupyterlab/apputils/lib/toolbar/widget.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docmanager-extension */ "webpack/sharing/consume/default/@jupyterlab/docmanager-extension");
/* harmony import */ var _jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _namepace__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./namepace */ "./lib/namepace.js");





function getToolbarItems(commands) {
    return [
        {
            name: 'save',
            factory: (widget) => _jupyterlab_docmanager_extension__WEBPACK_IMPORTED_MODULE_2__.ToolbarItems.createSaveButton(commands, widget.context.fileChanged)
        },
        { name: 'cut', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.cut },
        { name: 'copy', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.copy },
        { name: 'paste', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.paste },
        { name: 'duplicate', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.duplicate },
        { name: 'delete', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.del },
        { name: 'deleteAll', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.deleteAll },
        { name: 'run', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.run },
        { name: 'interrupt', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.interruptKernel },
        { name: 'restart', command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.restartKernel },
        {
            name: 'restart-and-run',
            command: _namepace__WEBPACK_IMPORTED_MODULE_3__.vp4jlCommandIDs.restartKernelAndRun
        },
        { name: 'spacer', type: 'spacer' },
        {
            name: 'kernelName',
            factory: (widget) => _jupyterlab_apputils_lib_toolbar__WEBPACK_IMPORTED_MODULE_4__.Toolbar.createKernelNameItem(widget.sessionContext)
        },
        {
            name: 'executionProgress',
            factory: (widget) => _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.ExecutionIndicator.createExecutionIndicatorItem(
            // @ts-ignore
            widget, undefined, undefined)
        }
    ];
}
function createWidget(widget, widgetFactory, item, defaultFactory) {
    return item.factory
        ? item.factory(widget)
        : defaultFactory(widgetFactory !== null && widgetFactory !== void 0 ? widgetFactory : '', widget, item);
}
function getToolbarFactory(commands, widgetFactory) {
    const toolbarItems = getToolbarItems(commands);
    const defaultFactory = (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.createDefaultFactory)(commands);
    return (widget) => {
        var _a;
        const toolbar = toolbarItems.map(item => ({
            name: item.name,
            widget: createWidget(widget, widgetFactory, item, defaultFactory)
        }));
        (_a = widget.model) === null || _a === void 0 ? void 0 : _a.setToolbarItems(toolbar);
        return toolbar;
    };
}


/***/ }),

/***/ "./lib/tracker.js":
/*!************************!*\
  !*** ./lib/tracker.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   IVPTrackerToken: () => (/* binding */ IVPTrackerToken),
/* harmony export */   VPTracker: () => (/* binding */ VPTracker)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);


const IVPTrackerToken = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('@jupyterlab/vp4jl:IVPTracker', `A widget tracker for visual programming files.
  Use this if you want to be able to iterate over and interact with file editors
  created by the application.`);
class VPTracker extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.WidgetTracker {
}


/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   isSameContent: () => (/* binding */ isSameContent)
/* harmony export */ });
function isSameContent(a, b) {
    const pureContentString = (content) => {
        let pure = content;
        if (typeof content === 'string') {
            pure = JSON.parse(content || 'null');
        }
        return JSON.stringify(pure);
    };
    const aContent = pureContentString(a);
    const bContent = pureContentString(b);
    return aContent === bContent;
}


/***/ }),

/***/ "./lib/visual-code-cell/actions.js":
/*!*****************************************!*\
  !*** ./lib/visual-code-cell/actions.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   changeCellType: () => (/* binding */ changeCellType)
/* harmony export */ });
/**
 * Change the selected cell type(s).
 *
 * @param notebook - The target notebook widget.
 *
 * @param value - The target cell type.
 *
 * #### Notes
 * It should preserve the widget mode.
 * This action can be undone.
 * The existing selection will be cleared.
 * Any cells converted to markdown will be unrendered.
 */
function changeCellType(notebook, value) {
    if (!notebook.model || !notebook.activeCell) {
        return;
    }
    const state = Private.getState(notebook);
    Private.changeCellType(notebook, value);
    Private.handleState(notebook, state);
}
/**
 * Change the selected cell type(s).
 *
 * @param notebook - The target notebook widget.
 *
 * @param value - The target cell type.
 *
 * #### Notes
 * It should preserve the widget mode.
 * This action can be undone.
 * The existing selection will be cleared.
 * Any cells converted to markdown will be unrendered.
 */
var Private;
(function (Private) {
    /**
     * Get the state of a widget before running an action.
     */
    function getState(notebook) {
        var _a, _b;
        return {
            wasFocused: notebook.node.contains(document.activeElement),
            activeCellId: (_b = (_a = notebook.activeCell) === null || _a === void 0 ? void 0 : _a.model.id) !== null && _b !== void 0 ? _b : null
        };
    }
    Private.getState = getState;
    /**
     * Handle the state of a widget after running an action.
     */
    function handleState(notebook, state, scrollIfNeeded = false) {
        const { activeCell, activeCellIndex } = notebook;
        if (state.wasFocused || notebook.mode === 'edit') {
            notebook.activate();
        }
        if (scrollIfNeeded && activeCell) {
            notebook.scrollToItem(activeCellIndex, 'smart', 0.05).catch(reason => {
                // no-op
            });
        }
    }
    Private.handleState = handleState;
    function changeCellType(notebook, value) {
        const notebookSharedModel = notebook.model.sharedModel;
        notebook.widgets.forEach((child, index) => {
            if (!notebook.isSelectedOrActive(child)) {
                return;
            }
            const differentType = child.model.type !== value;
            const differentCodeType = child.model.type === value && value === 'code';
            if (differentType || differentCodeType) {
                const raw = child.model.toJSON();
                notebookSharedModel.transact(() => {
                    notebookSharedModel.deleteCell(index);
                    if (value === 'code') {
                        // After change of type outputs are deleted so cell can be trusted.
                        raw.metadata.trusted = true;
                    }
                    else {
                        // Otherwise clear the metadata as trusted is only "valid" on code
                        // cells (since other cell types cannot have outputs).
                        raw.metadata.trusted = undefined;
                    }
                    const newCell = notebookSharedModel.insertCell(index, {
                        cell_type: value,
                        source: raw.source,
                        metadata: raw.metadata
                    });
                    if (raw.attachments && ['markdown', 'raw'].includes(value)) {
                        newCell.attachments =
                            raw.attachments;
                    }
                });
            }
            if (value === 'markdown') {
                // Fetch the new widget and unrender it.
                child = notebook.widgets[index];
                child.rendered = false;
            }
        });
        notebook.deselectAll();
    }
    Private.changeCellType = changeCellType;
})(Private || (Private = {}));


/***/ }),

/***/ "./lib/visual-code-cell/cell-type-item.js":
/*!************************************************!*\
  !*** ./lib/visual-code-cell/cell-type-item.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (/* binding */ createCellTypeItem)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _actions__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./actions */ "./lib/visual-code-cell/actions.js");





/**
 * The class name added to toolbar cell type dropdown wrapper.
 */
const TOOLBAR_CELLTYPE_CLASS = 'jp-Notebook-toolbarCellType';
/**
 * The class name added to toolbar cell type dropdown.
 */
const TOOLBAR_CELLTYPE_DROPDOWN_CLASS = 'jp-Notebook-toolbarCellTypeDropdown';
/**
 * A toolbar widget that switches cell types.
 * Only add a new `visual code` option in the dropdown to the code from
 * https://github.com/jupyterlab/jupyterlab/blob/a0d07f17e85acd967e722a5c5ed54529a361e5cf/packages/notebook/src/default-toolbar.tsx#L316
 */
class CellTypeSwitcher extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ReactWidget {
    /**
     * Construct a new cell type switcher.
     */
    constructor(widget, translator) {
        super();
        /**
         * Handle `change` events for the HTMLSelect component.
         */
        this.handleChange = (event) => {
            if (event.target.value !== '-') {
                let changeTo = event.target.value;
                this._notebook.widgets.forEach((child, index) => {
                    if (this._notebook.isSelectedOrActive(child)) {
                        if (changeTo === 'visual code') {
                            child.model.setMetadata('code type', changeTo);
                            changeTo = 'code';
                        }
                        else {
                            child.model.deleteMetadata('code type');
                        }
                    }
                });
                (0,_actions__WEBPACK_IMPORTED_MODULE_4__.changeCellType)(this._notebook, changeTo);
                this._notebook.activate();
            }
        };
        /**
         * Handle `keydown` events for the HTMLSelect component.
         */
        this.handleKeyDown = (event) => {
            if (event.keyCode === 13) {
                this._notebook.activate();
            }
        };
        this._trans = (translator || _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_3__.nullTranslator).load('jupyterlab');
        this.addClass(TOOLBAR_CELLTYPE_CLASS);
        this._notebook = widget;
        if (widget.model) {
            this.update();
        }
        widget.activeCellChanged.connect(this.update, this);
        // Follow a change in the selection.
        widget.selectionChanged.connect(this.update, this);
    }
    render() {
        var _a;
        let value = '-';
        if (this._notebook.activeCell) {
            value = this._notebook.activeCell.model.type;
        }
        let multipleSelected = false;
        for (const widget of this._notebook.widgets) {
            if (this._notebook.isSelectedOrActive(widget)) {
                if (widget.model.type !== value) {
                    value = '-';
                    multipleSelected = true;
                    break;
                }
            }
        }
        if (!multipleSelected &&
            ((_a = this._notebook.activeCell) === null || _a === void 0 ? void 0 : _a.model.getMetadata('code type')) ===
                'visual code') {
            value = 'visual code';
        }
        return (react__WEBPACK_IMPORTED_MODULE_0__.createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_1__.HTMLSelect, { className: TOOLBAR_CELLTYPE_DROPDOWN_CLASS, onChange: this.handleChange, onKeyDown: this.handleKeyDown, value: value, "aria-label": this._trans.__('Cell type'), title: this._trans.__('Select the cell type') },
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: "-" }, "-"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: "code" }, this._trans.__('Code')),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: "visual code" }, 'Visual Code'),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: "markdown" }, this._trans.__('Markdown')),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("option", { value: "raw" }, this._trans.__('Raw'))));
    }
}
/**
 * Create a cell type switcher item.
 *
 * #### Notes
 * It will display the type of the current active cell.
 * If more than one cell is selected but are of different types,
 * it will display `'-'`.
 * When the user changes the cell type, it will change the
 * cell types of the selected cells.
 * It can handle a change to the context.
 */
function createCellTypeItem(panel) {
    return new CellTypeSwitcher(panel.content);
}


/***/ }),

/***/ "./lib/visual-code-cell/content-factory.js":
/*!*************************************************!*\
  !*** ./lib/visual-code-cell/content-factory.js ***!
  \*************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ContentFactory: () => (/* binding */ ContentFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _editor_factory__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./editor-factory */ "./lib/visual-code-cell/editor-factory.js");
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./notebook */ "./lib/visual-code-cell/notebook.js");



class ContentFactory extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.NotebookPanel.ContentFactory {
    constructor(options) {
        super(options);
        this._editorFactories = {};
        this._editorFactories['code'] = options.editorFactory;
        this._editorFactories['visual code'] = _editor_factory__WEBPACK_IMPORTED_MODULE_1__.VisualCodeEditorFactory;
    }
    createNotebook(options) {
        return new _notebook__WEBPACK_IMPORTED_MODULE_2__.VPNotebook(options);
    }
    createCodeCell(options) {
        const opts = options;
        if (options.model.getMetadata('code type') === 'visual code') {
            opts.contentFactory = new ContentFactory({
                editorFactory: this._editorFactories['visual code']
            });
        }
        else if (options.contentFactory.editorFactory !== this._editorFactories['code']) {
            opts.contentFactory = new ContentFactory({
                editorFactory: this._editorFactories['code']
            });
        }
        return super.createCodeCell(opts);
    }
}


/***/ }),

/***/ "./lib/visual-code-cell/editor-factory.js":
/*!************************************************!*\
  !*** ./lib/visual-code-cell/editor-factory.js ***!
  \************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VisualCodeEditorFactory: () => (/* binding */ VisualCodeEditorFactory)
/* harmony export */ });
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./editor */ "./lib/visual-code-cell/editor.js");

const VisualCodeEditorFactory = (options) => {
    options.host.dataset.type = 'inline';
    return new _editor__WEBPACK_IMPORTED_MODULE_0__.VisualCodeEditor(options);
};


/***/ }),

/***/ "./lib/visual-code-cell/editor.js":
/*!****************************************!*\
  !*** ./lib/visual-code-cell/editor.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   EDITOR_CLASS: () => (/* binding */ EDITOR_CLASS),
/* harmony export */   VisualCodeEditor: () => (/* binding */ VisualCodeEditor)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./widget */ "./lib/visual-code-cell/widget.js");



const EDITOR_CLASS = 'jp-VPEditor';
class VisualCodeEditor {
    constructor(options) {
        var _a;
        /**
         * A signal emitted when either the top or bottom edge is requested.
         */
        this.edgeRequested = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal(this);
        this._isDisposed = false;
        this._uuid = '';
        this._options = {};
        const host = (this.host = options.host);
        host.classList.add(EDITOR_CLASS);
        host.classList.add('jp-Editor');
        host.addEventListener('focus', this, false);
        host.addEventListener('blur', this, false);
        this._uuid = (_a = options.uuid) !== null && _a !== void 0 ? _a : _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.UUID.uuid4();
        this._model = options.model;
        this._editor = (0,_widget__WEBPACK_IMPORTED_MODULE_2__.createVPWidget)(this._uuid, this._model, host);
    }
    get uuid() {
        return this._uuid;
    }
    set uuid(value) {
        this._uuid = value;
    }
    get editor() {
        return this._editor;
    }
    /**
     * Get the number of lines in the editor.
     */
    get lineCount() {
        return 0;
    }
    /**
     * Returns a model for this editor.
     */
    get model() {
        return this._model;
    }
    get lineHeight() {
        return 0;
    }
    get charWidth() {
        return 0;
    }
    /**
     * Tests whether the editor is disposed.
     */
    get isDisposed() {
        return this._isDisposed;
    }
    /**
     * Dispose of the resources held by the widget.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this.host.removeEventListener('focus', this, true);
        this.host.removeEventListener('blur', this, true);
        this.host.removeEventListener('scroll', this, true);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_1__.Signal.clearData(this);
    }
    /**
     * Get a config option for the editor.
     */
    getOption(option) {
        return this._options[option];
    }
    /**
     * Whether the option exists or not.
     */
    hasOption(option) {
        return Object.keys(this._options).indexOf(option) > -1;
    }
    /**
     * Set a config option for the editor.
     */
    setOption(option, value) {
        this._options[option] = value;
    }
    /**
     * Set config options for the editor.
     *
     * This method is preferred when setting several options. The
     * options are set within an operation, which only performs
     * the costly update at the end, and not after every option
     * is set.
     */
    setOptions(options) {
        for (const key in options) {
            this._options[key] = options[key];
        }
    }
    injectExtension(ext) { }
    /**
     * Returns the content for the given line number.
     */
    getLine(line) {
        return undefined;
    }
    /**
     * Find an offset for the given position.
     */
    getOffsetAt(position) {
        return 0;
    }
    /**
     * Find a position for the given offset.
     */
    getPositionAt(offset) {
        return { line: 0, column: 0 };
    }
    /**
     * Undo one edit (if any undo events are stored).
     */
    undo() {
        this.model.sharedModel.undo();
    }
    /**
     * Redo one undone edit.
     */
    redo() {
        this.model.sharedModel.redo();
    }
    /**
     * Clear the undo history.
     */
    clearHistory() {
        this.model.sharedModel.clearUndoHistory();
    }
    /**
     * Brings browser focus to this editor text.
     */
    focus() {
        this._editor.focus();
    }
    /**
     * Test whether the editor has keyboard focus.
     */
    hasFocus() {
        return this._editor.hasFocus;
    }
    /**
     * Explicitly blur the editor.
     */
    blur() {
        this._editor.contentDOM.blur();
    }
    get state() {
        throw new Error('Method not implemented yet');
    }
    getRange(from, to, separator) {
        return '';
    }
    /**
     * Reveal the given position in the editor.
     */
    revealPosition(position) { }
    /**
     * Reveal the given selection in the editor.
     */
    revealSelection(selection) { }
    /**
     * Get the window coordinates given a cursor position.
     */
    getCoordinateForPosition(position) {
        return {
            top: 0,
            left: 0,
            bottom: 0,
            right: 0,
            height: 0,
            width: 0,
            x: 0,
            y: 0,
            toJSON: () => ''
        };
    }
    /**
     * Get the cursor position given window coordinates.
     *
     * @param coordinate - The desired coordinate.
     *
     * @returns The position of the coordinates, or null if not
     *   contained in the editor.
     */
    getPositionForCoordinate(coordinate) {
        return null;
    }
    /**
     * Returns the primary position of the cursor, never `null`.
     */
    getCursorPosition() {
        return { line: 0, column: 0 };
    }
    /**
     * Set the primary position of the cursor.
     *
     * #### Notes
     * This will remove any secondary cursors.
     */
    setCursorPosition(position, options) { }
    /**
     * Returns the primary selection, never `null`.
     */
    getSelection() {
        return this.getSelections()[0];
    }
    /**
     * Set the primary selection. This will remove any secondary cursors.
     */
    setSelection(selection) {
        this.setSelections([selection]);
    }
    /**
     * Gets the selections for all the cursors, never `null` or empty.
     */
    getSelections() {
        throw new Error('Method not implemented yet');
    }
    /**
     * Sets the selections for all the cursors, should not be empty.
     * Cursors will be removed or added, as necessary.
     * Passing an empty array resets a cursor position to the start of a document.
     */
    setSelections(selections) { }
    /**
     * Replaces the current selection with the given text.
     *
     * Behaviour for multiple selections is undefined.
     *
     * @param text The text to be inserted.
     */
    replaceSelection(text) { }
    /**
     * Get a list of tokens for the current editor text content.
     */
    getTokens() {
        return [];
    }
    /**
     * Get the token at a given editor position.
     */
    getTokenAt(offset) {
        return { value: '', offset: 0, type: '' };
    }
    /**
     * Get the token a the cursor position.
     */
    getTokenAtCursor() {
        return this.getTokenAt(this.state.selection.main.head);
    }
    /**
     * Insert a new indented line at the current cursor position.
     */
    newIndentedLine() { }
    /**
     * Execute a codemirror command on the editor.
     *
     * @param command - The name of the command to execute.
     */
    execCommand(command) { }
    onKeydown(event) {
        return false;
    }
    /**
     * Handle the DOM events for the editor.
     *
     * @param event - The DOM event sent to the editor.
     *
     * #### Notes
     * This method implements the DOM `EventListener` interface and is
     * called in response to events on the editor's DOM node. It should
     * not be called directly by user code.
     */
    handleEvent(event) {
        switch (event.type) {
            case 'focus':
                this._evtFocus(event);
                break;
            case 'blur':
                this._evtBlur(event);
                break;
            default:
                break;
        }
    }
    _evtFocus(event) {
        this.host.classList.add('jp-mod-focused');
    }
    _evtBlur(event) {
        this.host.classList.remove('jp-mod-focused');
    }
}


/***/ }),

/***/ "./lib/visual-code-cell/execute.js":
/*!*****************************************!*\
  !*** ./lib/visual-code-cell/execute.js ***!
  \*****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   enhanceCodeCellExecute: () => (/* binding */ enhanceCodeCellExecute),
/* harmony export */   execute: () => (/* binding */ execute)
/* harmony export */ });
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Execute a cell given a client session.
 */
async function execute(cell, sessionContext, metadata) {
    var _a, _b;
    const model = cell.model;
    const isVisualCode = model.getMetadata('code type') === 'visual code';
    let code = '';
    const currentKernel = (_a = sessionContext.session) === null || _a === void 0 ? void 0 : _a.kernel;
    currentKernel === null || currentKernel === void 0 ? void 0 : currentKernel.registerCommTarget('capture_image', (comm, msg) => {
        comm.onMsg = (msg) => {
            // Base64-encoded image data
            const imageDomId = msg.content.data.image_dom_id;
            const imageData = msg.content.data.image_data;
            const imageElement = document.getElementById(imageDomId);
            if (imageElement) {
                imageElement.src = `data:image/png;base64,${imageData}`;
            }
            else {
                console.error(`image element ${imageDomId} not found, cannot set display intermediate image`);
            }
        };
    });
    if (isVisualCode && cell.editor) {
        const result = cell.editor.editor.getCode();
        if (result.hasError) {
            cell.outputArea.model.clear();
            cell.outputArea.model.add({
                output_type: 'error',
                ename: 'Error',
                evalue: result.result,
                traceback: []
            });
            return;
        }
        else {
            code = result.code;
        }
    }
    else {
        code = model.sharedModel.getSource();
    }
    if (!code.trim() || !((_b = sessionContext.session) === null || _b === void 0 ? void 0 : _b.kernel)) {
        model.sharedModel.transact(() => {
            model.clearExecution();
        }, false);
        return;
    }
    const cellId = { cellId: model.sharedModel.getId() };
    metadata = {
        ...model.metadata,
        ...metadata,
        ...cellId
    };
    const { recordTiming } = metadata;
    model.sharedModel.transact(() => {
        model.clearExecution();
        cell.outputHidden = false;
    }, false);
    cell.setPrompt('*');
    model.trusted = true;
    let future;
    try {
        const msgPromise = _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_1__.OutputArea.execute(code, cell.outputArea, sessionContext, metadata);
        // cell.outputArea.future assigned synchronously in `execute`
        if (recordTiming) {
            const recordTimingHook = (msg) => {
                let label;
                switch (msg.header.msg_type) {
                    case 'status':
                        label = `status.${msg.content.execution_state}`;
                        break;
                    case 'execute_input':
                        label = 'execute_input';
                        break;
                    default:
                        return true;
                }
                // If the data is missing, estimate it to now
                // Date was added in 5.1: https://jupyter-client.readthedocs.io/en/stable/messaging.html#message-header
                const value = msg.header.date || new Date().toISOString();
                const timingInfo = Object.assign({}, model.getMetadata('execution'));
                timingInfo[`iopub.${label}`] = value;
                model.setMetadata('execution', timingInfo);
                return true;
            };
            cell.outputArea.future.registerMessageHook(recordTimingHook);
        }
        else {
            model.deleteMetadata('execution');
        }
        // Save this execution's future so we can compare in the catch below.
        future = cell.outputArea.future;
        const msg = (await msgPromise);
        model.executionCount = msg.content.execution_count;
        if (recordTiming) {
            const timingInfo = Object.assign({}, model.getMetadata('execution'));
            const started = msg.metadata.started;
            // Started is not in the API, but metadata IPyKernel sends
            if (started) {
                timingInfo['shell.execute_reply.started'] = started;
            }
            // Per above, the 5.0 spec does not assume date, so we estimate is required
            const finished = msg.header.date;
            timingInfo['shell.execute_reply'] = finished || new Date().toISOString();
            model.setMetadata('execution', timingInfo);
        }
        return msg;
    }
    catch (e) {
        // If we started executing, and the cell is still indicating this
        // execution, clear the prompt.
        if (future && !cell.isDisposed && cell.outputArea.future === future) {
            cell.setPrompt('');
        }
        throw e;
    }
}
function enhanceCodeCellExecute() {
    // monkey patch the execute method of CodeCell
    _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_0__.CodeCell.execute = execute;
}


/***/ }),

/***/ "./lib/visual-code-cell/index.js":
/*!***************************************!*\
  !*** ./lib/visual-code-cell/index.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _cell_type_item__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./cell-type-item */ "./lib/visual-code-cell/cell-type-item.js");
/* harmony import */ var _content_factory__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./content-factory */ "./lib/visual-code-cell/content-factory.js");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _notebook__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./notebook */ "./lib/visual-code-cell/notebook.js");
/* harmony import */ var _execute__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./execute */ "./lib/visual-code-cell/execute.js");








const vp4jlVpCell = {
    id: 'vp4jlVpCell',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IToolbarWidgetRegistry, _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorServices, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_2__.INotebookWidgetFactory],
    activate: activateVp4jlVpCell
};
function activateVp4jlVpCell(app, toolbarRegistry, editorServices, notebookWidgetFactory) {
    const FACTORY = 'Notebook';
    toolbarRegistry.addFactory(FACTORY, 'cellType', panel => (0,_cell_type_item__WEBPACK_IMPORTED_MODULE_4__["default"])(panel));
    const editorFactory = editorServices.factoryService.newInlineEditor;
    notebookWidgetFactory.contentFactory = new _content_factory__WEBPACK_IMPORTED_MODULE_5__.ContentFactory({
        editorFactory
    });
    (0,_execute__WEBPACK_IMPORTED_MODULE_6__.enhanceCodeCellExecute)();
}
const vp4jlCloseMenuWhenCloseTab = {
    id: 'vp4jl:CloseMenuWhenCloseTab',
    autoStart: true,
    requires: [_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    activate: activateVp4jlCloseMenuWhenCloseTab
};
function activateVp4jlCloseMenuWhenCloseTab(app, labShell) {
    // close the context menu when switch the tab
    labShell.currentChanged.connect((_, args) => {
        const NotebookPanel = args.oldValue;
        const content = NotebookPanel === null || NotebookPanel === void 0 ? void 0 : NotebookPanel.content;
        if (content && content instanceof _notebook__WEBPACK_IMPORTED_MODULE_7__.VPNotebook) {
            content.closeMenus();
        }
    });
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ([vp4jlVpCell, vp4jlCloseMenuWhenCloseTab]);


/***/ }),

/***/ "./lib/visual-code-cell/notebook.js":
/*!******************************************!*\
  !*** ./lib/visual-code-cell/notebook.js ***!
  \******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VPNotebook: () => (/* binding */ VPNotebook)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _editor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./editor */ "./lib/visual-code-cell/editor.js");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__);



const NB_CELL_CLASS = 'jp-Notebook-cell';
class VPNotebook extends _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.Notebook {
    isVisualCodeCell(widget) {
        return widget.node.querySelectorAll(`.${_editor__WEBPACK_IMPORTED_MODULE_2__.EDITOR_CLASS}`).length > 0;
    }
    activate() {
        super.activate();
        this.closeMenus();
    }
    onResize(msg) {
        super.onResize(msg);
        this.closeMenus();
    }
    closeMenus() {
        for (let i = 0; i < this.widgets.length; i++) {
            const widget = this.widgets[i];
            if (this.isVisualCodeCell(widget)) {
                widget.editor.editor.closeMenu();
            }
        }
    }
    handleEvent(event) {
        if (!this.model) {
            return;
        }
        switch (event.type) {
            case 'mousedown':
                if (event.eventPhase === Event.CAPTURING_PHASE) {
                    this.evtMouseDownCapture(event);
                    this.closeMenus();
                }
                else {
                    super.handleEvent(event);
                }
                break;
            default:
                super.handleEvent(event);
                break;
        }
    }
    /**
     * Find the cell index containing the target html element.
     *
     * #### Notes
     * Returns -1 if the cell is not found.
     */
    findCell(node) {
        // Trace up the DOM hierarchy to find the root cell node.
        // Then find the corresponding child and select it.
        let n = node;
        while (n && n !== this.node) {
            if (n.classList.contains(NB_CELL_CLASS)) {
                const i = _lumino_algorithm__WEBPACK_IMPORTED_MODULE_1__.ArrayExt.findFirstIndex(this.widgets, widget => widget.node === n);
                if (i !== -1) {
                    return i;
                }
                break;
            }
            n = n.parentElement;
        }
        return -1;
    }
    /**
     * Find the target of html mouse event and cell index containing this target.
     *
     * #### Notes
     * Returned index is -1 if the cell is not found.
     */
    findEventTargetAndCell(event) {
        let target = event.target;
        let index = this.findCell(target);
        if (index === -1) {
            // `event.target` sometimes gives an orphaned node in Firefox 57, which
            // can have `null` anywhere in its parent line. If we fail to find a cell
            // using `event.target`, try again using a target reconstructed from the
            // position of the click event.
            target = document.elementFromPoint(event.clientX, event.clientY);
            index = this.findCell(target);
        }
        return [target, index];
    }
    /**
     * Handle `mousedown` event in the capture phase for the widget.
     */
    evtMouseDownCapture(event) {
        var _a;
        const { button, shiftKey } = event;
        const [target, index] = this.findEventTargetAndCell(event);
        const widget = this.widgets[index];
        // On OS X, the context menu may be triggered with ctrl-left-click. In
        // Firefox, ctrl-left-click gives an event with button 2, but in Chrome,
        // ctrl-left-click gives an event with button 0 with the ctrl modifier.
        if (button === 2 &&
            !shiftKey &&
            widget &&
            ((_a = widget.editorWidget) === null || _a === void 0 ? void 0 : _a.node.contains(target)) &&
            !this.isVisualCodeCell(widget)) {
            this.mode = 'command';
            // Prevent CodeMirror from focusing the editor.
            // TODO: find an editor-agnostic solution.
            event.preventDefault();
        }
    }
}


/***/ }),

/***/ "./lib/visual-code-cell/widget.js":
/*!****************************************!*\
  !*** ./lib/visual-code-cell/widget.js ***!
  \****************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VPWidget: () => (/* binding */ VPWidget),
/* harmony export */   createVPWidget: () => (/* binding */ createVPWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! vprcs */ "webpack/sharing/consume/default/vprcs/vprcs");
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(vprcs__WEBPACK_IMPORTED_MODULE_3__);




function isSerializedGraph(object) {
    return (object &&
        typeof object === 'object' &&
        Array.isArray(object.nodes) &&
        Array.isArray(object.edges));
}
class VPWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(id, model) {
        super();
        this._editor_activated = false;
        this._sceneActions = null;
        this.id = id;
        this.node.style.width = '100%';
        this.node.style.height = '100%';
        this.node.addEventListener('contextmenu', e => {
            e.preventDefault();
            e.stopPropagation();
        });
        this.node.addEventListener('focusout', function (e) {
            e.preventDefault();
            const nextFocusedElement = e.relatedTarget;
            const isElementChild = this.contains(nextFocusedElement);
            const isMenu = nextFocusedElement === null || nextFocusedElement === void 0 ? void 0 : nextFocusedElement.classList[0].includes('Mui');
            if (nextFocusedElement && (isElementChild || isMenu)) {
                e.stopPropagation();
            }
        });
        this._model = model;
    }
    get sharedModel() {
        return this._model.sharedModel;
    }
    setSceneActions(actions) {
        this._sceneActions = actions;
    }
    closeMenu() {
        var _a;
        (_a = this._sceneActions) === null || _a === void 0 ? void 0 : _a.closeMenu();
    }
    get hasFocus() {
        return this._editor_activated;
    }
    focus() {
        if (!this._editor_activated) {
            this._editor_activated = true;
            this.update();
        }
    }
    blur() {
        if (this._editor_activated) {
            this._editor_activated = false;
            this.update();
        }
    }
    get content() {
        let source = undefined;
        try {
            source = JSON.parse(this.sharedModel.getSource());
        }
        catch (e) {
            source = undefined;
        }
        return isSerializedGraph(source) ? source : null;
    }
    setContent(newContent) {
        if (this.sharedModel.getSource() !== newContent) {
            this.sharedModel.setSource(newContent);
        }
    }
    getCode() {
        var _a;
        return (_a = this._sceneActions) === null || _a === void 0 ? void 0 : _a.sourceCode();
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(vprcs__WEBPACK_IMPORTED_MODULE_3__.VPEditor, { id: this.id, content: this.content, onContentChange: this.setContent.bind(this), activated: this._editor_activated, onSceneActionsInit: this.setSceneActions.bind(this), option: {
                minimap: {
                    collapsed: true
                }
            } }));
    }
}
function createVPWidget(id, model, host) {
    const editor = new VPWidget(id, model);
    host.style.height = '300px';
    host.style.overflow = 'auto';
    host.style.resize = 'vertical';
    window.requestAnimationFrame(() => {
        if (host.isConnected) {
            _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget.attach(editor, host);
        }
    });
    return editor;
}


/***/ }),

/***/ "./lib/widget-factory.js":
/*!*******************************!*\
  !*** ./lib/widget-factory.js ***!
  \*******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   VPWidgetFactory: () => (/* binding */ VPWidgetFactory)
/* harmony export */ });
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");


class VPWidgetFactory extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_0__.ABCWidgetFactory {
    constructor(options, rendermime) {
        super(options);
        // the main widget is main area of the jupyter lab
        this._mainWidget = null;
        this._widgets = [];
        this._widgetId = 0;
        this._onMouseDown = this.deactivateWidgetIfMouseDownOut.bind(this);
        this._rendermime = rendermime;
    }
    createNewWidget(context) {
        context.model.setRendermime(this._rendermime);
        const w = new _widget__WEBPACK_IMPORTED_MODULE_1__.VPWidget(`vp_widget_${++this._widgetId}`, context);
        this.onWidgetCreated(w);
        w.disposed.connect(w => {
            this.onWidgetDisposed(w);
        });
        window.requestAnimationFrame(this._addEventListenerToTab.bind(this));
        return w;
    }
    deactivateWidgetIfMouseDownOut(event) {
        for (const w of this._widgets) {
            const rect = w.node.getBoundingClientRect();
            const hidden = !rect ||
                (rect.x === 0 && rect.y === 0 && rect.width === 0 && rect.height === 0);
            if (hidden) {
                continue;
            }
            const isInWidget = rect.x <= event.clientX &&
                event.clientX <= rect.x + rect.width &&
                rect.y <= event.clientY &&
                event.clientY <= rect.y + rect.height;
            if (!isInWidget) {
                w.content.deactivate();
            }
            else {
                w.content.activate();
            }
        }
    }
    onWidgetCreated(w) {
        var _a;
        this._widgets.push(w);
        if (this._mainWidget === null) {
            this._mainWidget = document.getElementById('main');
        }
        if (this._widgets.length === 1) {
            (_a = this._mainWidget) === null || _a === void 0 ? void 0 : _a.addEventListener('mousedown', this._onMouseDown);
            this._addEventListeners();
        }
    }
    onWidgetDisposed(widget) {
        var _a;
        this._widgets.splice(this._widgets.indexOf(widget), 1);
        if (this._widgets.length === 0) {
            (_a = this._mainWidget) === null || _a === void 0 ? void 0 : _a.removeEventListener('mousedown', this._onMouseDown);
            this._removeEventListeners();
        }
    }
    // hack way
    _addEventListeners() {
        // onPanelContextMenu from vp editor stop propagation
        document.addEventListener('contextmenu', this._onMouseDown);
        const sideBars = document.getElementsByClassName('jp-SideBar');
        for (let i = 0; i < sideBars.length; i++) {
            const sideBar = sideBars[i];
            for (const tab of sideBar.getElementsByClassName('lm-TabBar-tab')) {
                tab.addEventListener('click', this._onMouseDown);
            }
        }
        const menuBar = document.getElementById('jp-top-panel');
        const menus = menuBar === null || menuBar === void 0 ? void 0 : menuBar.getElementsByClassName('lm-MenuBar-item');
        for (const menu of menus || []) {
            menu.addEventListener('click', this._onMouseDown);
        }
    }
    _addEventListenerToTab() {
        // When click on the other tab of the main area, the currentChanged(index.ts) will be triggered.
        // We only need to add the click event listener to the tab corresponding to the current widget
        const dockPanel = document.getElementById('jp-main-dock-panel');
        (dockPanel === null || dockPanel === void 0 ? void 0 : dockPanel.getElementsByClassName('lm-mod-current')[0]).addEventListener('click', this._onMouseDown);
    }
    _removeEventListeners() {
        document.removeEventListener('contextmenu', this._onMouseDown);
        const sideBars = document.getElementsByClassName('jp-SideBar');
        for (let i = 0; i < sideBars.length; i++) {
            const sideBar = sideBars[i];
            for (const tab of sideBar.getElementsByClassName('button')) {
                tab.removeEventListener('click', this._onMouseDown);
            }
        }
        const menuBar = document.getElementById('jp-top-panel');
        const menus = menuBar === null || menuBar === void 0 ? void 0 : menuBar.getElementsByClassName('lm-MenuBar-item');
        for (const menu of menus || []) {
            menu.removeEventListener('click', this._onMouseDown);
        }
    }
}


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   ToolbarButton: () => (/* binding */ ToolbarButton),
/* harmony export */   VPEditorWidget: () => (/* binding */ VPEditorWidget),
/* harmony export */   VPMainAreaPanel: () => (/* binding */ VPMainAreaPanel),
/* harmony export */   VPOutputArea: () => (/* binding */ VPOutputArea),
/* harmony export */   VPWidget: () => (/* binding */ VPWidget)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! vprcs */ "webpack/sharing/consume/default/vprcs/vprcs");
/* harmony import */ var vprcs__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(vprcs__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var vprcs_dist_style_css__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! vprcs/dist/style.css */ "./node_modules/vprcs/dist/style.css");








class VPEditorWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(id, model) {
        super();
        this._editor_activated = false;
        this.id = id;
        this._model = model;
        this._model.vpContentChanged.connect(this.update, this);
    }
    get model() {
        return this._model;
    }
    activate() {
        if (!this._editor_activated) {
            this._editor_activated = true;
            this.update();
        }
    }
    deactivate() {
        if (this._editor_activated) {
            this._editor_activated = false;
            this.update();
        }
    }
    _updateToolbar() {
        // from toolbar-factory.tsx
        ['copy', 'paste', 'cut', 'duplicate', 'delete'].forEach(name => {
            this.model.toolbarItems[name].widget.update();
        });
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_5___default().createElement(vprcs__WEBPACK_IMPORTED_MODULE_6__.VPEditor, { id: this.id, content: this._model.vpContent, onContentChange: this._model.setVpContent.bind(this._model), activated: this._editor_activated, onSceneActionsInit: this._model.setVpActions.bind(this._model), onSelectionChange: this._updateToolbar.bind(this) }));
    }
}
class ToolbarButton extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ReactWidget {
    constructor(icon, label, tooltip, onClick) {
        super();
        this.icon = icon;
        this.label = label;
        this.tooltip = tooltip;
        this.onClick = onClick;
    }
    render() {
        return (react__WEBPACK_IMPORTED_MODULE_5___default().createElement(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.ToolbarButtonComponent, { icon: this.icon, label: this.label, tooltip: this.tooltip, onClick: this.onClick }));
    }
}
function createCloseButtion(click) {
    return new ToolbarButton(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.closeIcon, 'Close', 'Close the output window', click);
}
function createClearButtion(click) {
    return new ToolbarButton(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.clearIcon, 'Clear', 'Clear the output window', click);
}
class VPOutputAreaToolbar extends _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Toolbar {
    constructor() {
        super();
        this.addClass('jp-vp-output-area-toolbar');
        this._createToolbarItems();
    }
    _createToolbarItems() {
        this.addItem('spacer', _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_3__.Toolbar.createSpacerItem());
        this.addItem('clear', createClearButtion(() => { var _a; return (_a = this.parent) === null || _a === void 0 ? void 0 : _a.clear(); }));
        this.addItem('close', createCloseButtion(() => { var _a; return (_a = this.parent) === null || _a === void 0 ? void 0 : _a.hide(); }));
    }
}
class VPOutputArea extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget {
    constructor(id, model, sessionContext) {
        super({
            content: new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputArea({
                // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
                rendermime: model.rendermime,
                model: model.outputAreaModel
            }),
            toolbar: new VPOutputAreaToolbar()
        });
        this.sessionContext = sessionContext;
        this.id = id + 'output';
        this.addClass('jp-vp-output-area');
        this.title.label = 'Output';
    }
    showErrorMsg(msg) {
        this.content.model.clear();
        this.content.model.add({
            output_type: 'error',
            ename: 'Error',
            evalue: msg,
            traceback: []
        });
    }
    execute(code) {
        // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
        _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_2__.OutputArea.execute(code, this.content, this.sessionContext).catch(reason => {
            this.showErrorMsg(reason.message);
            return;
        });
    }
    clear() {
        this.content.model.clear();
    }
    toggleOutput() {
        this.isHidden ? this.show() : this.hide();
    }
}
class VPMainAreaPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_4__.SplitPanel {
    constructor(id, model, sessionContext) {
        super({ orientation: 'vertical', spacing: 1 });
        this._model = undefined;
        this.id = id + 'panel';
        this._model = model;
        this._sessionContext = sessionContext;
        this.addClass('jp-vp-main-area-panel');
        this._vpEditor = new VPEditorWidget(id, model);
        this.addWidget(this._vpEditor);
        this._outputArea = new VPOutputArea(id, model, sessionContext);
        this.addWidget(this._outputArea);
        this.setRelativeSizes([4, 1]);
    }
    activate() {
        if (this._vpEditor) {
            this._vpEditor.activate();
        }
    }
    deactivate() {
        if (this._vpEditor) {
            this._vpEditor.deactivate();
        }
    }
    execute() {
        var _a, _b;
        const sourceCode = (_b = (_a = this._model) === null || _a === void 0 ? void 0 : _a.vpActions) === null || _b === void 0 ? void 0 : _b.sourceCode();
        if (!sourceCode) {
            return;
        }
        if (sourceCode.messages.length > 0) {
            this._outputArea.showErrorMsg(sourceCode.messages[0].message);
        }
        else {
            this._outputArea.execute(sourceCode.code);
        }
    }
    toggleOutput() {
        this._outputArea.toggleOutput();
    }
    get sessionContext() {
        return this._sessionContext;
    }
}
class VPWidget extends _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_1__.DocumentWidget {
    constructor(id, context) {
        super({
            context,
            content: new VPMainAreaPanel(id, context.model, context.sessionContext)
        });
        this.title.iconClass = 'jp-VPIcon';
        this.title.caption = 'Visual Programming';
        this.addClass('jp-VPWidget');
        this.toolbar.addClass('jp-vp-toolbar');
        this.context.ready.then(this._onContextReady.bind(this));
        this.model.kernelSpecChanged.connect(this._changeKernel, this);
        this.sessionContext.kernelChanged.connect(this._setModelKernelSpec, this);
        this.context.saveState.connect(this._onSave, this);
    }
    get model() {
        return this.context.model;
    }
    get sessionContext() {
        return this.context.sessionContext;
    }
    execute() {
        this.content.execute();
    }
    toggleOutput() {
        this.content.toggleOutput();
    }
    _onContextReady() {
        this.sessionContext.kernelPreference = {
            canStart: true,
            shouldStart: true,
            autoStartDefault: false,
            shutdownOnDispose: false
        };
    }
    async _changeKernel(sender, newSpec) {
        if (newSpec) {
            this.sessionContext.changeKernel(newSpec);
        }
    }
    _setModelKernelSpec(sender, args) {
        void this.model.setKernelSpec(args.newValue);
    }
    _onSave(sender, state) {
        if (state === 'started' && this.model) {
            this.model.saveOutputModel();
        }
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_jupyterlab_statedb-webpack_sharing_consume_defau-4f409b.4d5c5c28464c9e5d2181.js.map