/*
 * selectors.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { kShinyApp, kQuartoApp } from '../../src/constants';

// Jupyter selectors
export const s_launcherTab = 'div[role="main"] >> text=Launcher';

// RStudio extension selectors
export const s_rsHomeIcon = '#rsw-icon';
export const s_rsProxiedServersHeader = 'div header#title_component_Proxied_Servers';
export const s_rsSidebarIcon = 'li[data-id="Posit-Workbench-tab"]';
export const s_rsWidget = '.jp-PositWorkbenchWidget';

// Expected proxied server labels
export const s_shinyServer =  `text="resources - ${kShinyApp}"`;
export const s_quartoServer =  `text="resources - ${kQuartoApp}"`;

