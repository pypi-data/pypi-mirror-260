/*
 * proxy-shiny-server.spec.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { test, expect } from '@jupyterlab/galata';

import * as cp from '../helpers/command-palette';
import * as term from '../helpers/terminal';
import { s_launcherTab, s_rsSidebarIcon, s_shinyServer } from '../helpers/selectors';
import { kShinyApp } from '../../src/constants';

test.describe('Posit side bar widget tests', () => {

  test.afterEach(async ({ page }) => {
    await term.sendInterruptToTerminal(page);
    await cp.closeAllTabs(page);
    await page.click(s_rsSidebarIcon);
  });

  test('Servers started before Proxied Servers view opened should appear in list (Shiny)', async({ page }) => {
    await cp.openNewTerminal(page);
    await term.sendTextToTerminal(page, 'cd ./resources; Rscript -e "shiny::runApp()"');
    await page.click(s_rsSidebarIcon); // open view
    await expect(page.locator(s_shinyServer).first()).toHaveText( `resources - ${kShinyApp}`, { timeout: 60000 });
  });

});

