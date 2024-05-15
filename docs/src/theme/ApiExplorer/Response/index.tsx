import React from 'react';
import Response from '@theme-original/ApiExplorer/Response';
import type ResponseType from '@theme/ApiExplorer/Response';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof ResponseType>;

export default function ResponseWrapper(props: Props): JSX.Element {
  return (
    <>
      {/* <Response {...props} /> */}
    </>
  );
}
