import { test } from 'node:test';
import assert from 'node:assert/strict';

import { routeToSlug } from './lighthouse-sweep.mjs';

test('routeToSlug converts routes to stable slugs', () => {
  assert.equal(routeToSlug('/'), 'home');
  assert.equal(routeToSlug('/about'), 'about');
  assert.equal(routeToSlug('/about/team'), 'about-team');
});