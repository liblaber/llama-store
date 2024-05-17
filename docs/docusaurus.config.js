// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require('prism-react-renderer/themes/github');
const darkCodeTheme = require('prism-react-renderer/themes/dracula');

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'liblab Llama Store',
  tagline: 'Llamas are cool',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-docusaurus-test-site.com',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'liblab', // Usually your GitHub org/user name.
  projectName: 'llama-store', // Usually your repo name.

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'throw',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
            docLayoutComponent: "@theme/DocPage",
            docItemComponent: "@theme/ApiItem" // derived from docusaurus-theme-openapi-docs
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  plugins: [
    [
      'docusaurus-plugin-openapi-docs',
      {
        id: "api", // plugin id
        docsPluginId: "classic", // id of plugin-content-docs or preset for rendering docs
        config: {
          llamastore: { // the <id> referenced when running CLI commands
            specPath: "../spec.yaml", // path to OpenAPI spec, URLs supported
            outputDir: "docs/API", // output directory for generated files
            sidebarOptions: { // optional, instructs plugin to generate sidebar.js
              groupPathsBy: "tag", // group sidebar items by operation "tag"
            },
          },
        }
      },
    ]
  ],
  themes: ["docusaurus-theme-openapi-docs"], // export theme components

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      
      navbar: {
        title: 'liblab Llama Store',
        logo: {
          alt: 'liblab Logo',
          src: 'img/logo.svg',
          href: 'https://github.com/liblaber/llama-store',
          srcDark: 'img/logo-dark.svg',
        },
        items: [
          {
            to: 'https://developers.liblab.com?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            label: 'Docs',
            position: 'right',
            rel: '',
          },
          {
            to: 'https://blog.liblab.com?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            label: 'Blog',
            position: 'right',
            rel: '',
          },
          {
            to: 'https://liblab.com/join?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            label: 'Get Started',
            position: 'right',
            rel: '',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            label: 'Discord',
            to: 'https://discord.gg/CnMRJMfHQc',
          },
          {
            label: 'GitHub',
            to: 'https://github.com/liblaber',
          },
          {
            label: 'YouTube',
            to: 'https://youtube.com/@liblaber',
          },
          {
            label: 'Twitter',
            to: 'https://twitter.com/liblaber',
          },
          {
            label: 'LinkedIn',
            to: 'https://www.linkedin.com/company/liblaber',
          },
          {
            label: 'liblab.com',
            to: 'https://liblab.com/?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            rel: '',
          },
          {
            label: 'About',
            to: 'https://liblab.com/about?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            rel: '',
          },
          {
            label: 'Blog',
            to: 'https://blog.liblab.com?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            rel: '',
          },
          {
            label: 'Contact us',
            to: 'https://liblab.com/contact?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            rel: '',
          },
          {
            label: 'Careers',
            to: 'https://liblab.com/careers?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            rel: '',
          },
          {
            label: 'Terms',
            to: 'https://liblab.com/terms?utm_source=llama-store&utm_medium=content&utm_campaign=none',
            rel: '',
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} liblab, Inc.`,
      },
      colorMode: {
        defaultMode: 'dark',
        disableSwitch: false,
        respectPrefersColorScheme: true,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: [
          'bash',
          'csharp',
          'graphql',
          'go',
          'java',
          'json',
          'log',
          'powershell',
          'toml',
          'yaml',
          'php',
        ],
      },
      languageTabs: [
        {
          highlight: "csharp",
          language: "csharp",
          codeSampleLanguage: "csharp",
          logoClass: "csharp",
          variant: "none",
          variants: ["none"],
        },
        {
          highlight: "go",
          language: "go",
          codeSampleLanguage: "go",
          logoClass: "go",
          variant: "none",
          variants: ["none"],
        },
        {
          highlight: "php",
          language: "php",
          codeSampleLanguage: "php",
          logoClass: "php",
          variant: "none",
          variants: ["none"],
        },
        {
          highlight: "python",
          language: "python",
          codeSampleLanguage: "python",
          logoClass: "python",
          variant: "none",
          variants: ["none"],
        },
      ],
    }),
};

module.exports = config;
