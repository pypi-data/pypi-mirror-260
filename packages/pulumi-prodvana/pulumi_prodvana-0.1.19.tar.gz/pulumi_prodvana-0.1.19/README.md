# Prodvana Resource Provider

The Prodvana Resource Provider lets you manage [Prodvana](http://prodvana.io) resources.

## Installing

This package is available for several languages/platforms:

### Node.js (JavaScript/TypeScript)

To use from JavaScript or TypeScript in Node.js, install using either `npm`:

```bash
npm install @prodvana/pulumi-prodvana
```

or `yarn`:

```bash
yarn add @prodvana/pulumi-prodvana
```

### Python

To use from Python, install using `pip`:

```bash
pip install pulumi_prodvana
```

### Go

To use from Go, use `go get` to grab the latest version of the library:

```bash
go get github.com/prodvana/pulumi-prodvana/sdk/go/...
```

### .NET

To use from .NET, install using `dotnet add package`:

```bash
dotnet add package Pulumi.Prodvana
```

## Configuration

The following configuration points are available for the `prodvana` provider:

- `prodvana:apiToken` (environment: `PVN_API_TOKEN`) - An API token generated with permissions to this organization.
- `prodvana:orgSlug` (environment: `PVN_ORG_SLUG`) - Prodvana organization to authenticate with (you can find this in your Org's url: <org_slug>.prodvana.io) 

## Reference

For detailed reference documentation, please visit [the Pulumi registry](https://www.pulumi.com/registry/packages/prodvana/api-docs/).
