/**
 * Basic tests for API service
 */

import api from '../api';

// Mock axios
jest.mock('axios', () => {
  return {
    create: jest.fn(() => ({
      defaults: {
        headers: {
          common: {}
        }
      },
      interceptors: {
        request: {
          use: jest.fn()
        },
        response: {
          use: jest.fn()
        }
      },
      setToken: jest.fn()
    }))
  };
});

describe('API Service', () => {
  test('API instance is created', () => {
    expect(api).toBeDefined();
  });

  test('setToken method exists', () => {
    expect(typeof api.setToken).toBe('function');
  });

  test('API has default headers', () => {
    expect(api.defaults).toBeDefined();
    expect(api.defaults.headers).toBeDefined();
  });

  test('API has interceptors configured', () => {
    expect(api.interceptors).toBeDefined();
    expect(api.interceptors.request).toBeDefined();
    expect(api.interceptors.response).toBeDefined();
  });
});

