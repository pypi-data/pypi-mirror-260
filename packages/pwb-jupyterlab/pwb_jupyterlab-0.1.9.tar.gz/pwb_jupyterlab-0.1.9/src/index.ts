/*
 * index.ts
 *
 * Copyright (C) 2022 by Posit Software, PBC
 *
 */

import rstudioHome from '../images/posit-icon-fullcolor.svg';
import rstudioPanel from '../images/posit-icon-unstyled.svg';

import { PositWorkbenchWidget } from './widget';

import { Panel, Widget } from '@lumino/widgets';
import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import { LabIcon } from '@jupyterlab/ui-components';
import { ServerConnection } from '@jupyterlab/services';
import { heartbeat, stopHeartbeat } from './disconnectMonitor';
import { setupDisconnectNotification } from './disconnectAlert';

let homeUrl: string = '/home';

const rstudioIcon = new LabIcon({
  name: 'pwb_jupyterlab:home-icon',
  svgstr: rstudioHome,
});

const rstudioPanelIcon = new LabIcon({
  name: 'pwb_jupyterlab:panel-icon',
  svgstr: rstudioPanel,
});

function returnHome(): void {
  location.assign(homeUrl);
}

function registerCommands(app: JupyterFrontEnd, palette: ICommandPalette): void {
  var regex = /(s\/[\w]{5}[\w]{8}[\w]{8}\/)/g;
  const settings = ServerConnection.makeSettings();
  homeUrl = settings.baseUrl.replace(regex, 'home/');

  // Register command to return to Posit Workbench home
  const command = 'pwb_jupyterlab:return-home';
  app.commands.addCommand(command, {
    label: 'Return to Posit Workbench Home',
    caption: 'Return to Posit Workbench Home',
    execute: returnHome
  });
  palette.addItem({ command, category: 'Posit Workbench' });
}

function addPositIcon(app: JupyterFrontEnd): void {
  // Add Posit icon that returns the user to home to menu bar
  const rstudio_widget = new Widget();
  rstudio_widget.id = 'rsw-icon';
  rstudio_widget.node.onclick = returnHome;

  rstudioIcon.element({
    container: rstudio_widget.node,
    margin: '2px 5px 2px 5px',
    height: 'auto',
    width: '20px',
  });
  app.shell.add(rstudio_widget, 'top', { rank: 1 });
}

function addSideBar(app: JupyterFrontEnd): void{
  // Add the RSW side bar widget to the left panel
  const panel = new Panel();
  panel.id = 'Posit-Workbench-tab';
  panel.title.icon = rstudioPanelIcon;
  panel.addWidget(new PositWorkbenchWidget());
  app.shell.add(panel, 'left', { rank: 501 });
}

function activate(app: JupyterFrontEnd, palette: ICommandPalette) {
  registerCommands(app, palette);
  addPositIcon(app);
  addSideBar(app);
  heartbeat(returnHome);
  setupDisconnectNotification();
}

function deactivate() {
  stopHeartbeat();
}

/**
 * Initialization data for the pwb_jupyterlab extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'pwb_jupyterlab:plugin',
  description: 'Enhance experience of running JupyterLab in Posit Workbench.',
  autoStart: true,
  requires: [ICommandPalette],
  activate: activate,
  deactivate: deactivate
};

export default plugin;
