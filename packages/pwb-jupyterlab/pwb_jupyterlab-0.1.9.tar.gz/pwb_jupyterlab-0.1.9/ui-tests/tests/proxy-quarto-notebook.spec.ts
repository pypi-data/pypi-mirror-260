/*
 * proxy-quarto-server.spec.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { test, expect } from '@jupyterlab/galata';

import * as cp from '../helpers/command-palette';
import * as term from '../helpers/terminal';
import { s_rsSidebarIcon, s_quartoServer, s_rsWidget, s_rsProxiedServersHeader } from '../helpers/selectors';
import { kQuartoApp } from '../../src/constants';

test.describe('Posit side bar widget tests', () => {

  test.beforeEach(async ({ page }) => {
    await page.click(s_rsSidebarIcon); // open proxied servers view
  });

  test.afterEach(async ({ page }) => {
    await term.sendInterruptToTerminal(page);
    await page.click(s_rsSidebarIcon); // close proxied servers view
    await cp.closeAllTabs(page);
  });

  test('Servers should appear in Proxied Servers view (Quarto / Notebook)', async({ page }) => {
    await cp.openNewTerminal(page);
    await term.sendTextToTerminal(page, 'cd ./resources; quarto preview ./basics-jupyter.ipynb');
    await expect(page.locator(s_quartoServer).first()).toHaveText(`resources - ${kQuartoApp}`, { timeout: 60000 });
  });
});

