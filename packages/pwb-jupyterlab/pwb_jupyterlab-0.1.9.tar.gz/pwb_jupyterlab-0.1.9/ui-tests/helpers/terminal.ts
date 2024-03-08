/*
 * terminal.ts
 *
 * Copyright (C) 2024 by Posit Software, PBC
 *
 */

import { Page } from '@playwright/test';

export async function sendTextToTerminal(page: Page, text: string) {
    const term = page.locator('textarea[aria-label="Terminal input"]')
    await term.fill(text);
    await term.press('Enter');
}

export async function sendInterruptToTerminal(page: Page) {
    const term = page.locator('textarea[aria-label="Terminal input"]')
    await term.press('Control+C');
}
