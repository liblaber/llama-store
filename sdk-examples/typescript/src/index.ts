import { Llamastore } from 'llamastore';

const sdk = new Llamastore({ accessToken: process.env.LLAMASTORE_ACCESS_TOKEN });

(async () => {
  const result = await sdk.llama.getLlamas();
  console.log(result);
})();
