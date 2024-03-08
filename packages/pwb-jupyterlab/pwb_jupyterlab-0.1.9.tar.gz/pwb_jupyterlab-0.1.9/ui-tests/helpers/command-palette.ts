/*
 * command-palette.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { Page } from "@playwright/test";

async function openCommandPalette(page: Page) {
  await page.locator('div .lm-MenuBar-itemLabel >> text=View').click();
  await page.click('text=Activate Command Palette');
}

export async function passCommandToCommandPalette(page: Page, command: string) {
  await openCommandPalette(page);
  await page.fill(
    '[aria-label="Command Palette Section"] [placeholder="SEARCH"]',
    command
  );
} 

export async function closeAllTabs(page: Page) {
  await passCommandToCommandPalette(page, 'Close All Tabs');
  await page.locator('li[data-command="application:close-all"]').click();
}

export async function openNewTerminal(page: Page) {
  await passCommandToCommandPalette(page, 'New Terminal');
  await page.locator('li[data-command="terminal:create-new"]').click();
}
