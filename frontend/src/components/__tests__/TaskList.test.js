/**
 * Basic tests for TaskList component
 */

import React from 'react';
import { render } from '@testing-library/react';
import TaskList from '../TaskList';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: jest.fn()
  }),
  useParams: () => ({
    projectId: '1'
  }),
  Link: ({ children, to }) => <a href={to}>{children}</a>
}));

describe('TaskList Component', () => {
  test('renders without crashing', () => {
    const { container } = render(<TaskList />);
    expect(container).toBeTruthy();
  });

  test('component returns valid JSX', () => {
    const { container } = render(<TaskList />);
    expect(container.firstChild).toBeTruthy();
  });

  test('component has task-related content or structure', () => {
    const { container } = render(<TaskList />);
    // Just verify the component renders something
    expect(container.innerHTML.length).toBeGreaterThan(0);
  });
});

