/**
 * This is a swizzled wrapper for the Request component.
 *
 * In this case, we want to hide the Request component, so we return an empty
 * JSX element.
 */
import React from "react";
import type RequestType from "@theme/ApiExplorer/Request";
import type { WrapperProps } from "@docusaurus/types";

type Props = WrapperProps<typeof RequestType>;

export default function RequestWrapper(props: Props): JSX.Element {
  return <>{/* <Request {...props} /> */}</>;
}
