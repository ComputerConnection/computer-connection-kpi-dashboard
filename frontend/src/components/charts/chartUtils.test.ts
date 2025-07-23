import { describe, it, expect } from 'vitest';
import { formatDate } from './chartUtils';

describe('chart utils', () => {
  it('formats date string', () => {
    expect(formatDate('2024-01-01')).toMatch(/2024/);
  });
});
