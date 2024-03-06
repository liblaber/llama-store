import { beforeEach } from 'mocha';
import { expect } from 'chai';
import CustomHook, { Request } from "../src/index";
import * as dotenv from 'dotenv';
import { assert } from 'console';

dotenv.config();

describe('test custom hook', () => {
  let hook = new CustomHook();

  beforeEach(() => {
    hook = new CustomHook();
  });

  it('empty passing test', async () => {

    const request: Request = {
      method: 'GET',
      url: 'https://api.example.com',
      input: {},
      headers: {
        'Content-Type': 'application/json',
      },
    };

    await hook.beforeRequest(request);
    console.log(request.headers)

    // Assert the headers are correct
    assert(request.headers['Content-Type'] === 'application/json');
  });
});
