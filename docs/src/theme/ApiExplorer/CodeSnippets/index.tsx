/**
 * This is a swizzled wrapper for the OpenAPI plugin theme
 * APIExplorer/CodeSnippets component.
 *
 * The goal of this is to replace the language sample with SDK code
 * generated by liblab. To use this, you need to have created JSON snippets
 * for your SDKs, and put this JSON in the static/snippets folder,
 * named as language.json, for example typescript.json.
 */

import React, { useState } from "react";

import useDocusaurusContext from "@docusaurus/useDocusaurusContext";

import ApiCodeBlock from "@theme/ApiExplorer/ApiCodeBlock";
import CodeTabs from "@theme/ApiExplorer/CodeTabs";
import type CodeSnippetsType from "@theme/ApiExplorer/CodeSnippets";
import type Language from "@theme/ApiExplorer/CodeSnippets/code-snippets-types";
import type { WrapperProps } from "@docusaurus/types";

type Props = WrapperProps<typeof CodeSnippetsType>;

/**
 * Renders a code tab component.
 *
 * This is a tab designed to contain code snippets, and is styled to
 * show the language icon and name. This is a child of the CodeTabs
 * component available from the OpenAPI plugin theme.
 *
 * @param children - The content to be displayed within the code tab.
 * @param hidden - A boolean indicating whether the code tab should be hidden.
 * @param className - Additional CSS classes to be applied to the code tab.
 * @returns The JSX element representing the code tab.
 */
function CodeTab({ children, hidden, className }: any): JSX.Element {
  return (
    <div role="tabpanel" className={className} {...{ hidden }}>
      {children}
    </div>
  );
}

/**
 * Renders a language code tab. This creates a code tab, with an API code block
 * containing the code snippet for the language.
 */
function LanguageCodeTab(language: Language): JSX.Element {
  return (
    <CodeTab
      value={language.language}
      label={language.language}
      key={language.language}
      attributes={{
        className: `openapi-tabs__code-item--${language.logoClass}`,
      }}
    >
      {/* @ts-ignore */}
      <ApiCodeBlock
        language={language.highlight}
        className="openapi-explorer__code-block"
        showLineNumbers={true}
      >
        {language.sample}
      </ApiCodeBlock>
    </CodeTab>
  );
}

function GetSnippetsForLanguage(language: Language, props: Props) {
  // load the snippets
  const snippets = require(`/snippets/${language.language}.json`);

  // convert the current API endpoint to the snippet name
  // in the same format as the snippets.
  // In this case, path parameters in the path name are `:name`, 
  // such as `:llamaId`, and we need these as `{llamaId}`.
  var endpoint = props.postman.url.path
    .map((p: string) => p.startsWith(":") ? `/{${p.replace(":", "")}}` : `/${p}`)
    .join("");

  // Get the sample and set it on the language object
  language.sample = snippets.endpoints[endpoint][props.postman.method.toLowerCase()];
}

/**
 * Renders the CodeSnippetsWrapper component.
 *
 * This is a wrapper for the swizzled CodeSnippets component, which
 * replaces the original component with a simpler one that shows
 * code snippets for the SDKs generated by liblab.
 *
 * @param {Props} props - The component props.
 * @returns {JSX.Element} The rendered component.
 */
export default function CodeSnippetsWrapper(props: Props): JSX.Element {
  const { siteConfig } = useDocusaurusContext();

  // Get the language tabs from the site config
  const langs = [...(siteConfig?.themeConfig?.languageTabs as Language[])];

  // Get the default language from local storage
  const defaultLang: Language[] = langs.filter(
    (lang) =>
      lang.language === localStorage.getItem("docusaurus.tab.code-samples")
  );

  // Set up state for the variant and sample - these are not used here,
  // but are required by the CodeTabs component from the OpenAPI plugin theme
  const [selectedVariant, setSelectedVariant] = useState<string | undefined>();
  const [selectedSample, setSelectedSample] = useState<string | undefined>();

  // Set up state for the language - this is used to track the currently
  // selected language
  const [language, setLanguage] = useState(() => defaultLang[0] ?? langs[0]);

  // Get the code snippet data for the selected language
  // These come from a generated JSON file in the static/snippets folder
  langs.forEach((language) => GetSnippetsForLanguage(language, props));

  // Render the code tabs with the language samples
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
        {langs.map((lang) => LanguageCodeTab(lang))}
      </CodeTabs>
    </>
  );
}
