/*
 * posit-side-bar.spec.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { test, expect } from '@jupyterlab/galata';

import { s_rsProxiedServersHeader, s_rsSidebarIcon, s_rsWidget } from '../helpers/selectors';

test.describe('Posit side bar widget tests', () => {

  test.beforeEach(async ({ page }) => {
    await page.locator(s_rsSidebarIcon).click();
  });

  test.afterEach(async ({ page }) => {
      await page.locator(s_rsSidebarIcon).click();
  });

  test('Workbench Proxied Servers header should be present', async({ page }) => {
    expect(await page.locator(s_rsWidget).isVisible()).toBe(true);
    expect(await page.locator(s_rsProxiedServersHeader).isVisible()).toBe(true);
  });

});

