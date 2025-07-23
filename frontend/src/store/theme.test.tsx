import { describe, it, expect } from 'vitest';
import { useThemeStore } from './theme';

describe('theme store', () => {
  it('toggles dark mode', () => {
    expect(useThemeStore.getState().dark).toBe(false);
    useThemeStore.getState().toggle();
    expect(useThemeStore.getState().dark).toBe(true);
  });
});
