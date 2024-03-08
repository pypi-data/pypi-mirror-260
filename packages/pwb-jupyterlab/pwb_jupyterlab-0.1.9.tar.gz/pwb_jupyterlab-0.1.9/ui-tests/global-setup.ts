/*
 * global-setup.ts
 *
 * Copyright (C) 2022 by Posit Software, PBC
 *
 */

// This file shares variables with './pwb_jupyterlab/constants.py'
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const { baseURL } = config.projects[0].use;
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(baseURL!);

  try {
    await page.locator('button:has-text("No Kernel")', { timeout: 5000 }).click();
  }
  catch(error) {
      // don't do anything, this popup may or may not appear
  }
}

export default globalSetup;
