import React, { useState } from "react";

import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

import ApiCodeBlock from "@theme/ApiExplorer/ApiCodeBlock";
import CodeTabs from "@theme/ApiExplorer/CodeTabs";
import type CodeSnippetsType from '@theme/ApiExplorer/CodeSnippets';
import type {CodeSample, Language} from "@theme/ApiExplorer/CodeSnippets/code-snippets-types";
import type {WrapperProps} from '@docusaurus/types';

type Props = WrapperProps<typeof CodeSnippetsType>;

function CodeTab({ children, hidden, className }: any): JSX.Element {
  return (
    <div role="tabpanel" className={className} {...{ hidden }}>
      {children}
    </div>
  );
}

export default function CodeSnippetsWrapper(props: Props): JSX.Element {

  const { siteConfig } = useDocusaurusContext();

  const langs = [
    ...((siteConfig?.themeConfig?.languageTabs as Language[])),
  ];

  const defaultLang: Language[] = langs.filter(
    (lang) =>
      lang.language === localStorage.getItem("docusaurus.tab.code-samples")
  );
  const [selectedVariant, setSelectedVariant] = useState<string | undefined>();
  const [selectedSample, setSelectedSample] = useState<string | undefined>();
  const [language, setLanguage] = useState(() => {
    // Return first index if only 1 user-defined language exists
    if (langs.length === 1) {
      return langs[0];
    }
    // Fall back to language in localStorage or first user-defined language
    return defaultLang[0] ?? langs[0];
  });

  const codeSamples = langs.map((language) => {
    const data = require(`/snippets/${language.language}.json`)

    // convert the path data to the snippet name
    var url = props.postman.url;
    var paths = url.path;
    var endpoint = "";
    paths.forEach((path: string) => {
      endpoint += "/"
      if (path.startsWith(":")) {
        endpoint += "{" + path.replace(":", "") + "}";
      } else {
        endpoint += path;
      }
    });

    language.sample = data.endpoints[endpoint][props.postman.method.toLowerCase()];

    const codeSample: CodeSample = {
      lang: language.language,
      source: data.endpoints[endpoint][props.postman.method.toLowerCase()],
    };

    return codeSample;
  });

  const newProps:Props = {
    postman: props.postman,
    codeSamples: codeSamples,
  };

  console.log(JSON.stringify(newProps))

  return (
    <>
      <CodeTabs
        groupId="code-samples"
        action={{
          setLanguage: setLanguage,
          setSelectedVariant: setSelectedVariant,
          setSelectedSample: setSelectedSample,
        }}
        languageSet={langs}
        lazy
      >
        {langs.map((lang) => {
          return (
            <CodeTab
              value={lang.language}
              label={lang.language}
              key={lang.language}
              attributes={{
                className: `openapi-tabs__code-item--${lang.logoClass}`,
              }}
            >
              {/* @ts-ignore */}
              <ApiCodeBlock
                language={lang.highlight}
                className="openapi-explorer__code-block"
                showLineNumbers={true}
              >
                {lang.sample}
              </ApiCodeBlock>
            </CodeTab>
          );
        })}
      </CodeTabs>
    </>
  );
}
