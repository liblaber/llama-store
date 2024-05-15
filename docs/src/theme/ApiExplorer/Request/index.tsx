import React from 'react';
import Request from '@theme-original/ApiExplorer/Request';
import type RequestType from '@theme/ApiExplorer/Request';
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof RequestType>;

export default function RequestWrapper(props: Props): JSX.Element {
  return (
    <>
      {/* <Request {...props} /> */}
    </>
  );
}
