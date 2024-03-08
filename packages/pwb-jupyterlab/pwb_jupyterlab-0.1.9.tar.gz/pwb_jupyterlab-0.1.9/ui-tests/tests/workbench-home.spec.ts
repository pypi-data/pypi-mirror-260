/*
 * workbench-home.spec.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { test, expect } from '@jupyterlab/galata';

import { s_rsHomeIcon } from '../helpers/selectors';
import { passCommandToCommandPalette } from '../helpers/command-palette';

test.describe('Posit Workbench home tests', () => {

  test('Posit Workbench home icon should be present', async({ page }) => {
    await expect(page.locator(s_rsHomeIcon).elementHandle()).toBeTruthy();
  });
  
  test('Posit Workbench return home command should be present', async ({
    page,
  }) => {
    await passCommandToCommandPalette(page, 'Posit Workbench');
    await expect(page.locator('.lm-CommandPalette-itemLabel >> text=Return to Posit Workbench Home').elementHandle()).toBeTruthy();
  });

});
