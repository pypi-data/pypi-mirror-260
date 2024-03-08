/*
 * proxy-quarto-server.spec.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { test, expect } from '@jupyterlab/galata';

import * as cp from '../helpers/command-palette';
import * as term from '../helpers/terminal';
import { s_rsSidebarIcon, s_quartoServer } from '../helpers/selectors';
import { kQuartoApp } from '../../src/constants';

test.describe('Posit side bar widget tests', () => {

  test.beforeEach(async ({ page }) => {
    await page.locator(s_rsSidebarIcon).click(); // open proxied servers view
  });

  test.afterEach(async ({ page }) => {
    await term.sendInterruptToTerminal(page);
    await page.click(s_rsSidebarIcon);
    await cp.closeAllTabs(page);
  });

  test('Servers should appear in Proxied Servers view (Quarto / QMD)', async({ page }) => {
    await cp.openNewTerminal(page);
    await term.sendTextToTerminal(page, 'cd ./resources; quarto preview ./hello.qmd');
    await expect(page.locator(s_quartoServer).first()).toHaveText(`resources - ${kQuartoApp}`, { timeout: 10000 });
  });
});

