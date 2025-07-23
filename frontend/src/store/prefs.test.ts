import { describe, it, expect } from 'vitest';
import { usePrefStore } from './prefs';

describe('prefs store', () => {
  it('toggleHidden adds and removes id', () => {
    usePrefStore.setState({ hidden: [] });
    usePrefStore.getState().toggleHidden('revenue');
    expect(usePrefStore.getState().hidden).toContain('revenue');
    usePrefStore.getState().toggleHidden('revenue');
    expect(usePrefStore.getState().hidden).not.toContain('revenue');
  });
});
