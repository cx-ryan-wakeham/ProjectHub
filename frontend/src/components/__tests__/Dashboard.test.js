/**
 * Basic tests for Dashboard component
 */

import React from 'react';
import { render } from '@testing-library/react';
import Dashboard from '../Dashboard';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: jest.fn()
  }),
  Link: ({ children, to }) => <a href={to}>{children}</a>
}));

describe('Dashboard Component', () => {
  test('renders without crashing', () => {
    const { container } = render(<Dashboard />);
    expect(container).toBeTruthy();
  });

  test('component returns valid JSX', () => {
    const { container } = render(<Dashboard />);
    expect(container.firstChild).toBeTruthy();
  });

  test('dashboard has content', () => {
    const { container } = render(<Dashboard />);
    const hasContent = container.textContent.length > 0 || container.querySelector('div, section, main');
    expect(hasContent).toBeTruthy();
  });
});

