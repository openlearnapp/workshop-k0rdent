# Workshop: k0rdent

## Purpose

Advanced IT workshop for platform engineers and Kubernetes administrators. Hands-on setup of [k0rdent](https://k0rdent.io) on Hetzner, managing templates, services, and multi-cluster deployments.

## Target Audience

- **Level**: Advanced — Kubernetes experience required
- **Prior knowledge**: kubectl, helm, basic cluster operations
- **Goal**: Run a production-grade k0rdent management cluster, deploy workload clusters

## Structure

- **11 lessons** covering the full k0rdent platform lifecycle
- **Interface language**: English (currently)
- **Teaching language**: English (en-US)
- **Features**: hands-on cloud setup, real infrastructure (Hetzner)

### Lessons

1. Welcome to k0rdent — overview
2. Setting Up the Management Cluster on Hetzner
3. Verifying & Exploring the Installation
4. The Templating System
5. Credentials & Access Management
6. Deploying Your First Cluster
7. Managing Cluster Lifecycle
8. Working with Services (KSM)
9. Multi-Cluster Services & Hosted Control Planes
10. Creating Custom Templates
11. Backup, Restore & Observability

## Labels

`IT` · `Kubernetes` · `Platform Engineering` · `Advanced`

## Conventions

- **Real infrastructure**: learners provision actual Hetzner servers
- **Commands in `q`**: what to run
- **Expected output/explanation in `a`**
- **Prerequisites**: each lesson references what must be set up first
- Linear progression — lessons build on each other

## Development

```bash
# Generate audio (Edge TTS)
bash generate-audio.sh english/k0rdent-workshop
```

## See Also

- [k0rdent Project](https://k0rdent.io)
- [Open Learn Platform](https://github.com/openlearnapp/openlearnapp.github.io)
- [Workshop Guide](https://github.com/openlearnapp/openlearnapp.github.io/blob/main/docs/workshop-guide.md)
- [Lesson Schema](https://github.com/openlearnapp/openlearnapp.github.io/blob/main/docs/lesson-schema.md)
- [Workshop Creator Plugin](https://github.com/openlearnapp/plugin-workshop-creator)
