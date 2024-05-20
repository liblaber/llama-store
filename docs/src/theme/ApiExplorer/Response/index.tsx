/**
 * This is a swizzled wrapper for the Response component.
 *
 * In this case, we want to hide the Response component, so we return an empty
 * JSX element.
 */

import React from "react";
import type ResponseType from "@theme/ApiExplorer/Response";
import type { WrapperProps } from "@docusaurus/types";

type Props = WrapperProps<typeof ResponseType>;

export default function ResponseWrapper(props: Props): JSX.Element {
  return <></>;
}
