/**
 * Basic tests for Login component
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import Login from '../Login';

// Mock react-router-dom
jest.mock('react-router-dom', () => ({
  useHistory: () => ({
    push: jest.fn()
  })
}));

describe('Login Component', () => {
  test('renders login form', () => {
    render(<Login />);
    
    // Check if login elements are present
    const loginElements = screen.queryAllByText(/login/i);
    expect(loginElements.length).toBeGreaterThan(0);
  });

  test('renders username input', () => {
    render(<Login />);
    
    // Look for username/email input field
    const inputs = document.querySelectorAll('input');
    expect(inputs.length).toBeGreaterThan(0);
  });

  test('renders password input', () => {
    render(<Login />);
    
    // Look for password input field
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    expect(passwordInputs.length).toBeGreaterThan(0);
  });

  test('renders submit button', () => {
    render(<Login />);
    
    // Look for button element
    const buttons = document.querySelectorAll('button');
    expect(buttons.length).toBeGreaterThan(0);
  });
});

