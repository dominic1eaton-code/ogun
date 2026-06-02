# ogun OS — Third-Party Integrations Specification
## Complete Integration Reference · Version 0.1.0-alpha

**ogun OS · Project Ogún · 2026**
**Document Type:** Integration Architecture & Feature Specification

---

## Integration Architecture Overview

**integrations planned for future Ogun OS releases**

ogun OS integrates third-party platforms and services through a structured, capability-gated architecture governed by the Elegua Protocol (IPC), the Ọpọn Protocol (cross-enterprise data isolation), and the ogun Capability Model. All third-party integrations are managed as **registered connectors** accessible from within the relevant Tier 4 User Apps and routed through the `ogun-subsystem-network` and Sambara agent system.

### How Integrations Work in ogun OS

**Integration Layer:** All third-party connections operate through explicitly declared capability grants in each app's `ogun-component.toml` manifest. No integration may access host OS APIs directly — all external calls are routed through the emulator's virtual network adapter (`ogun-virtual-network-adapter`) using OS sockets only.

**Data Isolation:** The Ọpọn Protocol (`SYS-001`) ensures that data from integrations attributed to Enterprise A is never accessible within the context of Enterprise B, even when both enterprises use the same third-party platform (e.g., two separate Stripe accounts for two different enterprises on the same ogun OS instance).

**Agent Automation:** Sambara agents can interact with integrations up to their declared authority level. No agent may trigger a financial transaction through an integration without `FinancialWrite` capability and valid attribution metadata.

**Namespace Routing:** Integration data surfaces in the semantic VFS under `enterprise://[id]/integrations/[service-name]/` and is addressable by all apps with appropriate capability grants.

**Connector Architecture:** Integrations are registered as typed connector objects within the relevant app's integration registry, discoverable via `opm` (ogun Package Manager) or built-in as first-party connectors within specific Tier 4 apps.

---

## Integration Categories

1. [Inbox & Communications](#1-inbox--communications)
2. [Content Creation & Podcasting](#2-content-creation--podcasting)
3. [Website & Storefront Builders](#3-website--storefront-builders)
4. [Payment & Financial Services](#4-payment--financial-services)
5. [Messaging & Community Platforms](#5-messaging--community-platforms)
6. [Social Media & Content Distribution](#6-social-media--content-distribution)
7. [Professional Networks & Forums](#7-professional-networks--forums)
8. [Publishing & Newsletters](#8-publishing--newsletters)
9. [Creator Monetization & Commerce](#9-creator-monetization--commerce)
10. [Freelance & Gig Marketplaces](#10-freelance--gig-marketplaces)
11. [On-Demand & Service Marketplaces](#11-on-demand--service-marketplaces)
12. [Field Service & Trade Tools](#12-field-service--trade-tools)
13. [Crowdfunding & Community Funding](#13-crowdfunding--community-funding)
14. [Investment & Equity Crowdfunding](#14-investment--equity-crowdfunding)
15. [Creator Subscription & Membership](#15-creator-subscription--membership)
16. [AI, Knowledge & Productivity Tools](#16-ai-knowledge--productivity-tools)
17. [Development & Code Hosting](#17-development--code-hosting)
18. [Project Management & Collaboration](#18-project-management--collaboration)
19. [Banking, Payments & Money Transfer](#19-banking-payments--money-transfer)
20. [Design & Creative Tools](#20-design--creative-tools)
21. [Calendar, Scheduling & CRM](#21-calendar-scheduling--crm)
22. [Writing & Document Tools](#22-writing--document-tools)
23. [Accounting & Finance Tools](#23-accounting--finance-tools)
24. [Website & Portfolio Builders](#24-website--portfolio-builders)
25. [Music & Audio Platforms](#25-music--audio-platforms)
26. [Delivery, Food & Logistics](#26-delivery-food--logistics)
27. [Video & Streaming Platforms](#27-video--streaming-platforms)
28. [Cloud Infrastructure](#28-cloud-infrastructure)

---

## 1. Inbox & Communications

---

### MyPublicInbox (`mypublicinbox`)

**Primary App:** `ayo` (Digital Spaces), `kogi` (Software-Defined Office), `heshima` (Identity)
**Integration Type:** Inbound communication channel connector
**Capability Required:** `ipc.write`, `network.outbound`

**What It Is:** MyPublicInbox is a managed public inbox service that allows creators, founders, and independent workers to receive messages, requests, and inbound inquiries through a public-facing endpoint without exposing a personal email address.

**How It Works in ogun OS:**

MyPublicInbox integrates with ogun OS as a **unified inbox connector** within `kogi`'s Filtering System. Inbound messages received through the operator's MyPublicInbox endpoint are pulled into the `ogun-messenger` unified inbox, classified by the Filtering System's priority rules, and surfaced in the Utility Bar's notification strip.

Within `ayo` (Digital Spaces), the operator's MyPublicInbox handle is embedded as a verified contact link in their public profile space and Linktree/Linknet (via `heshima`). This allows any visitor to their digital space to send a message without the operator's direct contact information being exposed.

**Sambara Agent Integration:** The FOLLOWUP_AGENT can monitor the MyPublicInbox feed for unanswered messages older than a configurable threshold and draft response suggestions for operator review at `RECOMMEND` authority.

**Functions on the Platform:**
- Receive and display inbound public messages within the unified messenger
- Route high-priority inquiries to the Kogi pipeline as new lead entries
- Surface as a contact method in Heshima identity profiles and Ayo spaces
- Feed inbound inquiry data to Qala for audience engagement analytics
- Allow the Acquisition Agent to monitor inquiry volume as a pipeline health signal

---

## 2. Content Creation & Podcasting

---

### Castmagic (`castmagic`)

**Primary App:** `akeel` (Knowledge Management), `shango` (Solution Factory), `ayo` (Digital Spaces)
**Integration Type:** AI content repurposing connector
**Capability Required:** `network.outbound`, `filesystem.write:artifact://`, `ipc.write:shango.*`

**What It Is:** Castmagic is an AI-powered platform that transforms audio and video content (podcasts, interviews, recordings) into written assets — show notes, transcripts, social posts, newsletters, blog posts, and more.

**How It Works in ogun OS:**

Castmagic connects to ogun OS as a **content production integration** within `shango`'s Production Pipeline. An operator uploading a recorded session (interview, podcast episode, client call, webinar) can trigger a Castmagic processing job directly from the Shango factory interface. The resulting repurposed assets — transcript, show notes, social snippets, newsletter draft, blog post — are returned as typed artifacts and registered in the VFS under `artifact://[enterprise-id]/content/[session-id]/`.

Within `akeel`, the transcript is indexed as a knowledge document, making the spoken content searchable within the operator's institutional memory system. Decisions, client insights, and methodology notes captured in audio form become part of the knowledge graph.

**Functions on the Platform:**
- Transform audio/video uploads into structured content artifacts from within Shango's production pipeline
- Auto-register repurposed content (transcripts, show notes, social copy) as named artifacts in the VFS
- Index transcript content into Akeel's knowledge base for semantic search
- Feed generated social copy directly to Ayo's content creation surface for scheduling and publishing
- Surface Castmagic as a tool binding available to the PRODUCTIZATION_AGENT when detectable audio content patterns suggest repurposable material
- Feed content production throughput metrics to Qala Observatory

---

## 3. Website & Storefront Builders

---

### Squarespace (`squarespace`)

**Primary App:** `ayo` (Digital Spaces), `zuri` (Digital Marketplace), `heshima` (Identity)
**Integration Type:** Web presence and commerce connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:zuri.*`

**What It Is:** Squarespace is a website-building and e-commerce platform used by creators, service providers, and small businesses to build and publish professional websites and online stores.

**How It Works in ogun OS:**

Squarespace integrates with ogun OS as a **web presence connector** within `ayo` (Digital Spaces). The operator's Squarespace site is registered as an external digital space within Ayo's Space Registry, and its key analytics (visitor traffic, page views, form submissions, sales conversions) are pulled into Qala's Observatory through the connector. This gives the operator a single view of their digital presence performance, including their Squarespace site alongside all other digital channels.

For e-commerce, Squarespace transactions are reconciled with `dongo`'s income streams. When a Squarespace sale occurs, the connector creates a corresponding income record attributed to the operator's digital products enterprise.

**Functions on the Platform:**
- Register the Squarespace site as a tracked external digital space within Ayo
- Pull site analytics (traffic, conversions, form submissions) into the Qala Observatory dashboard
- Sync Squarespace store orders into `zuri`'s order management registry
- Reconcile Squarespace revenue as attributed income streams in `dongo`
- Monitor site performance as a digital presence KPI in the Enzo enterprise dashboard
- Surface scheduling links and contact forms embedded in Squarespace to the Heshima Linktree/Linknet

---

### Wix (`wix`)

**Primary App:** `ayo`, `zuri`, `heshima`
**Integration Type:** Web presence and commerce connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:zuri.*`

**What It Is:** Wix is a cloud-based website building platform used by freelancers, creators, and small business owners to create websites, portfolios, and online stores.

**How It Works in ogun OS:** Identical integration architecture to Squarespace. The Wix connector registers the operator's Wix site as an external digital space in Ayo, pulls analytics into Qala, and reconciles Wix e-commerce revenue in Dongo. Wix booking appointments are synced into `misimu`'s calendar.

**Functions on the Platform:**
- Register Wix site as an external space in Ayo
- Pull traffic and conversion analytics into Qala
- Sync Wix Bookings appointments to Misimu calendar
- Reconcile Wix e-commerce revenue in Dongo
- Embed Wix contact and booking links in Heshima Linktree

---

### Carrd (`carrd`)

**Primary App:** `ayo`, `heshima`
**Integration Type:** Single-page web presence connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Carrd is a lightweight platform for building simple, responsive single-page sites — commonly used for landing pages, link-in-bio pages, and personal portfolios.

**How It Works in ogun OS:** Carrd integrates as a minimal web presence connector. The operator's Carrd page is registered in Ayo's Space Registry as a link-in-bio space. Link click analytics are pulled into Qala. Carrd form submissions are routed into the Kogi unified inbox as inbound leads.

**Functions on the Platform:**
- Register Carrd page as an external link-in-bio space in Ayo
- Pull link click analytics into Qala
- Route contact form submissions to Kogi as inbound inquiries
- Embed Carrd link in Heshima Linktree

---

### JournoPortfolio (`journoportfolio`)

**Primary App:** `ayo`, `heshima`, `akeel`
**Integration Type:** Portfolio publication connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** JournoPortfolio is a portfolio platform for journalists, writers, and content creators to showcase published work.

**How It Works in ogun OS:** Published work items from JournoPortfolio are synced into Akeel's knowledge base as external artifacts, making the operator's published canon part of their institutional memory and searchable alongside internal content. The portfolio page is registered as an external digital space in Ayo.

**Functions on the Platform:**
- Register JournoPortfolio as an external portfolio space in Ayo
- Sync published clippings and articles into Akeel knowledge base
- Surface portfolio links in Heshima identity profiles
- Feed publication volume metrics to Qala for content production tracking

---

## 4. Payment & Financial Services

---

### Square (`square`)

**Primary App:** `dongo` (Financial Management), `zuri` (Marketplace), `kogi`
**Integration Type:** Point-of-sale and payment processing connector
**Capability Required:** `financial.read`, `financial.write`, `network.outbound`

**What It Is:** Square is a payment processing and point-of-sale platform used by service businesses, contractors, and retailers for in-person and online payments.

**How It Works in ogun OS:**

Square connects to ogun OS as a **payment processing integration** within `dongo`'s Income Management system. Square transactions are automatically ingested as income records and attributed to the appropriate enterprise and engagement. The Square connector reads the transaction ledger via Square's API and presents items to Dongo's bank reconciliation workflow.

For service-based operators (contractors, trades, mobile service providers), Square card reader transactions sync directly to the corresponding job or engagement in `kogi`, automatically creating a payment-received event and updating the engagement's financial status.

**Functions on the Platform:**
- Ingest Square transactions as attributed income records in Dongo
- Auto-attribute payments to the corresponding engagement or project in Kogi
- Trigger payment-received events that update engagement lifecycle states
- Feed Square revenue data to Qala Observatory as income stream telemetry
- Support the Bookkeeping Agent's transaction reconciliation workflow
- Display Square balance and recent transactions on the Enzo enterprise dashboard
- Reconcile Square invoices with Dongo's accounts receivable module

---

### Stripe (`stripe`)

**Primary App:** `dongo`, `zuri`, `ume`, `shango`
**Integration Type:** Payment infrastructure and subscription billing connector
**Capability Required:** `financial.read`, `financial.write`, `network.outbound`

**What It Is:** Stripe is a payment infrastructure platform used by software companies, SaaS builders, digital product creators, and online businesses for payment processing, subscription billing, and marketplace payments.

**How It Works in ogun OS:**

Stripe is the primary payment infrastructure integration for digital product and SaaS enterprises managed in ogun OS. Within `dongo`, the Stripe connector ingests all charges, subscriptions, payouts, and refunds as structured financial records with full attribution. Stripe webhook events trigger real-time income record creation in Dongo's ledger.

Within `zuri`, Stripe serves as the default payment processor for Software-Defined Stores. When an operator creates a store in Zuri and lists digital products or services, Stripe handles checkout, and the resulting transactions are routed back to Dongo for financial recording and attribution.

Within `shango`, Stripe subscription data is used to track Monthly Recurring Revenue (MRR) at the product level — feeding the `shango` factory's revenue performance tracking and informing the Productization Agent's assessment of which products are scaling.

The Enzo enterprise dashboard displays Stripe MRR, new subscriptions, churn rate, and total payout as key financial health metrics.

**Functions on the Platform:**
- Ingest all Stripe charges, subscriptions, payouts, and refunds into Dongo's ledger
- Power payment processing for Zuri's Software-Defined Stores
- Track MRR and subscription metrics at the Shango product level
- Feed real-time revenue data to Qala Observatory and the Enzo enterprise dashboard
- Support automated quarterly tax reserve calculations in Dongo based on Stripe revenue
- Enable the Bookkeeping Agent to auto-reconcile Stripe transactions
- Support the PRICING_AGENT with product revenue history for pricing optimization
- Trigger engagement lifecycle events in Kogi on payment completion

---

### Venmo (`venmo`)

**Primary App:** `dongo`, `kogi`
**Integration Type:** P2P payment tracking connector
**Capability Required:** `financial.read`, `network.outbound`

**What It Is:** Venmo is a mobile peer-to-peer payment application used for sending and receiving money between individuals — often used by freelancers and gig workers for informal payment collection.

**How It Works in ogun OS:** Venmo connects to `dongo` as a P2P payment income source. Received Venmo payments are classified as income records with the corresponding enterprise and engagement attribution. The Bookkeeping Agent monitors unattributed Venmo inflows and prompts the operator to assign them to the correct engagement or income stream.

**Functions on the Platform:**
- Track received Venmo payments as income records in Dongo
- Surface unattributed Venmo income for the Bookkeeping Agent's reconciliation workflow
- Display Venmo balance in the unified Dongo accounts dashboard
- Attribute Venmo payments to Kogi engagements when memo field matches engagement IDs

---

### PayPal (`paypal`)

**Primary App:** `dongo`, `zuri`, `kogi`
**Integration Type:** Payment platform connector
**Capability Required:** `financial.read`, `financial.write`, `network.outbound`

**What It Is:** PayPal is a global digital payments platform used by freelancers, online sellers, and service businesses for invoicing, payment collection, and money transfer.

**How It Works in ogun OS:** PayPal integrates with `dongo` as a payment platform connector with read and write capability. Received PayPal payments are ingested as income records. PayPal invoices can be generated and sent from within `kogi`'s engagement management interface. For international engagements, PayPal's multi-currency support is mapped to Dongo's multi-currency wallet system.

**Functions on the Platform:**
- Ingest PayPal transactions as attributed income records in Dongo
- Generate and send PayPal invoices from within Kogi engagement management
- Reconcile PayPal payments with Dongo's accounts receivable
- Display PayPal balance in the unified accounts dashboard
- Support multi-currency transaction recording via Dongo's FX management

---

### Zelle (`zelle`)

**Primary App:** `dongo`
**Integration Type:** Bank-to-bank payment tracking connector
**Capability Required:** `financial.read`, `network.outbound`

**What It Is:** Zelle is a bank-to-bank digital payment network used in the US for fast money transfers, commonly used by freelancers, trades workers, and service providers.

**How It Works in ogun OS:** Zelle payments appear in bank account feeds connected through Dongo's bank aggregation layer. Received Zelle payments are classified and attributed to engagements through the Bookkeeping Agent's reconciliation workflow. Since Zelle operates bank-to-bank (no Zelle API is publicly available), integration is achieved through bank account transaction feed parsing.

**Functions on the Platform:**
- Detect and classify incoming Zelle payments from connected bank account feeds in Dongo
- Surface unattributed Zelle income for the Bookkeeping Agent's reconciliation
- Include Zelle income in Dongo's income stream tracking and reporting

---

### Chime (`chime`)

**Primary App:** `dongo`, `zamani`
**Integration Type:** Banking account connector
**Capability Required:** `financial.read`, `network.outbound`

**What It Is:** Chime is a US-based neobank offering checking accounts, savings accounts, and debit cards — commonly used by gig workers and independent contractors.

**How It Works in ogun OS:** Chime connects to `dongo` as a linked bank account through open banking connectors. Chime account balances, transaction history, and deposit records are pulled into Dongo's unified accounts dashboard. The Bookkeeping Agent monitors Chime accounts for income deposits and flags unattributed transactions.

**Functions on the Platform:**
- Display Chime balance and transaction history in the Dongo accounts dashboard
- Surface unattributed Chime deposits for Bookkeeping Agent reconciliation
- Support cash flow projection in Dongo using Chime balance data

---

## 5. Messaging & Community Platforms

---

### WhatsApp (`whatsapp`)

**Primary App:** `kogi`, `ogun-messenger`, `ayo`
**Integration Type:** Messaging and client communication connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** WhatsApp is a global messaging platform with over 2 billion users, widely used by independent workers for client communication, especially in international and small business contexts.

**How It Works in ogun OS:** WhatsApp connects to `kogi`'s Filtering System as a communication channel within the unified inbox. Messages from WhatsApp are surfaced in `ogun-messenger` with priority classification. Client inquiries received on WhatsApp can be converted to Kogi pipeline entries. The FOLLOWUP_AGENT can draft WhatsApp message responses for operator review.

For `ayo` (Digital Spaces), a WhatsApp click-to-chat link is embeddable in the operator's public spaces and Heshima Linktree.

**Functions on the Platform:**
- Surface WhatsApp messages in the ogun unified messenger
- Route WhatsApp client inquiries to Kogi as lead/engagement entries
- Allow the Follow-Up Agent to draft WhatsApp message responses at RECOMMEND authority
- Embed WhatsApp contact links in Ayo digital spaces and Heshima Linktree
- Track WhatsApp response time as a client engagement metric in Qala

---

### Discord (`discord`)

**Primary App:** `ayo`, `kogi`, `ogun-messenger`
**Integration Type:** Community platform and team communication connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Discord is a voice, video, and text communication platform widely used by creators, gaming communities, developer communities, and independent businesses for community building and team communication.

**How It Works in ogun OS:** Discord integrates with `ayo` as a community platform connector. Operators running community spaces (courses, mastermind groups, professional communities) can link their Discord server to an Ayo space and track member engagement, message volume, and active member count as community health metrics in Qala.

Discord notifications and direct messages are routed to `ogun-messenger`. The operator can configure priority rules in Kogi's Filtering System to surface specific Discord channels (e.g., customer support, new member alerts) as high-priority notifications.

**Functions on the Platform:**
- Link Discord server to an Ayo community space for member and engagement tracking
- Route Discord DMs and priority channel notifications to ogun-messenger
- Track Discord community health metrics (member count, activity, retention) in Qala Observatory
- Configure Kogi filtering rules to prioritize Discord alerts from specific channels
- Enable Sambara agents to monitor Discord for support requests at OBSERVE authority
- Embed Discord join links in Ayo spaces and Heshima identity profiles

---

### Telegram (`telegram`)

**Primary App:** `kogi`, `ogun-messenger`, `ayo`
**Integration Type:** Messaging and community connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Telegram is a cloud-based messaging platform used for personal messaging, group channels, and community broadcasting — especially popular among creator and crypto communities.

**How It Works in ogun OS:** Telegram integrates as a messaging and community channel connector. Telegram direct messages are surfaced in `ogun-messenger`. Telegram channel analytics (subscriber count, post reach, engagement) are pulled into Qala. Telegram group inquiries can be converted to Kogi pipeline entries.

**Functions on the Platform:**
- Surface Telegram DMs in the ogun unified messenger
- Pull Telegram channel subscriber count and engagement metrics into Qala
- Route channel inquiries to Kogi as leads
- Embed Telegram links in Ayo spaces and Heshima Linktree
- Enable broadcasting to Telegram channels from Ayo's content publishing interface

---

### Skool (`skool`)

**Primary App:** `ayo`, `zuri`, `dongo`, `kogi`
**Integration Type:** Online community and course platform connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:zuri.*`

**What It Is:** Skool is a community-building and online course platform combining paid memberships, structured courses, and community features in a single environment.

**How It Works in ogun OS:** Skool integrates with `ayo` as a managed community space. Member counts, engagement levels, and course completion rates are pulled into Qala as community health metrics. Skool subscription revenue is reconciled with `dongo` as a recurring income stream. New Skool member sign-ups can create engagement entries in Kogi.

**Functions on the Platform:**
- Register Skool community as a managed external space in Ayo
- Pull member engagement and course completion metrics into Qala Observatory
- Reconcile Skool subscription revenue as a recurring income stream in Dongo
- Create Kogi lead entries for high-value new member onboarding
- Track community churn and growth as Enzo enterprise KPIs

---

### Meetup (`meetup`)

**Primary App:** `misimu`, `ayo`, `kogi`
**Integration Type:** Event and community discovery connector
**Capability Required:** `network.outbound`, `ipc.write:misimu.*`

**What It Is:** Meetup is a platform for organizing in-person and online group events, commonly used by community organizers, professionals, and independent workers for networking and community building.

**How It Works in ogun OS:** Meetup integrates with `misimu` as an event management connector. Events created in Meetup are synced to the Misimu calendar. RSVP counts and attendee analytics are fed to Qala. Operator-hosted Meetup events are reflected in the Ayo digital space as public event listings.

**Functions on the Platform:**
- Sync Meetup events and RSVPs to Misimu calendar
- Pull event attendance analytics into Qala
- Display upcoming hosted events in Ayo community spaces
- Track networking event volume as a strategic activity metric

---

### Connectteams (`connectteams`)

**Primary App:** `kogi`, `ume`, `moto`
**Integration Type:** Team operations and field workforce connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Connecteams is an all-in-one app for managing deskless and field workforces — used by trades businesses, contractors, and small service companies for scheduling, time tracking, and team communication.

**How It Works in ogun OS:** Connecteams integrates with `kogi` for effort and schedule management and `ume` for HR and workforce management. Staff schedules are synced to Misimu. Time tracking data feeds into Dongo's payroll and expense tracking. Team communications surface in ogun-messenger.

**Functions on the Platform:**
- Sync Connecteams staff schedules to Misimu
- Pull time tracking records into Dongo for payroll and cost tracking
- Surface team communications in ogun-messenger
- Track team utilization and capacity in Kogi
- Feed workforce cost data to Enzo enterprise dashboards via Dongo

---

### Basecamp (`basecamp`)

**Primary App:** `moto`, `kogi`, `akeel`
**Integration Type:** Project management and team communication connector
**Capability Required:** `network.outbound`, `ipc.write:moto.*`

**What It Is:** Basecamp is a project management and team communication platform used by small businesses, agencies, and freelancers for managing client projects and team collaboration.

**How It Works in ogun OS:** Basecamp connects to `moto` as an external project management source. Basecamp projects, to-dos, and due dates are synced into Moto's work package registry. Basecamp messages are routed to ogun-messenger. Project documents are indexed in Akeel.

**Functions on the Platform:**
- Sync Basecamp projects and to-do lists into Moto's work package registry
- Route Basecamp messages and client updates to ogun-messenger
- Index Basecamp project documents in Akeel's knowledge base
- Pull Basecamp project status into Enzo enterprise dashboards
- Trigger Kogi engagement updates when Basecamp milestones complete

---

### Fanbase (`fanbase`)

**Primary App:** `ayo`, `zuri`, `dongo`
**Integration Type:** Creator monetization and fan community connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:zuri.*`

**What It Is:** Fanbase is a social media and fan monetization platform that allows creators to build paid subscriber communities and sell content directly to fans.

**How It Works in ogun OS:** Fanbase integrates with `ayo` as a managed creator community space and with `zuri` as a content commerce channel. Fanbase subscriber count and subscription revenue are tracked in the Enzo enterprise dashboard. Revenue is reconciled in Dongo.

**Functions on the Platform:**
- Register Fanbase as a managed community space in Ayo
- Sync Fanbase subscriber metrics to Qala Observatory
- Reconcile Fanbase subscription revenue in Dongo
- Display Fanbase community growth as an Enzo enterprise KPI

---

## 6. Social Media & Content Distribution

---

### X / Twitter (`x`, `twitter`)

**Primary App:** `ayo`, `heshima`, `qala`
**Integration Type:** Social media publishing and analytics connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** X (formerly Twitter) is a microblogging and social media platform used by creators, founders, and independent professionals for thought leadership, audience building, and client discovery.

**How It Works in ogun OS:** X connects to `ayo` as a social media publishing channel. Content drafted in Ayo's content creation interface (posts, threads, articles) can be published or scheduled to X. X analytics (follower count, impressions, engagement rate, profile visits) are pulled into Qala Observatory as audience growth metrics.

The Sambara agent system can monitor X mention and DM volumes at OBSERVE authority, surfacing engagement signals to the Observatory. The ACQUISITION_AGENT can identify prospect engagement signals from X interactions at RECOMMEND authority.

**Functions on the Platform:**
- Publish and schedule content to X from Ayo's content interface
- Pull follower count, impressions, and engagement metrics into Qala Observatory
- Surface X analytics as digital presence KPIs in Enzo enterprise dashboard
- Route X DMs and mentions to ogun-messenger for monitoring
- Embed X profile link in Heshima Linktree and Ayo digital spaces
- Enable the Acquisition Agent to flag prospect engagement signals at RECOMMEND

---

### Instagram (`instagram`)

**Primary App:** `ayo`, `heshima`, `qala`
**Integration Type:** Social media publishing and analytics connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Instagram is a photo and video sharing platform with strong creator and small business monetization tools, including shopping, subscriptions, and paid partnerships.

**How It Works in ogun OS:** Instagram connects to `ayo` as a visual content publishing and social commerce channel. Posts, Reels, and Stories can be drafted and scheduled from Ayo's content creation interface. Instagram analytics (followers, reach, impressions, story views, shop conversions) are pulled into Qala. Instagram shop revenue is reconciled with Dongo.

**Functions on the Platform:**
- Draft, schedule, and publish Instagram posts, Reels, and Stories from Ayo
- Pull Instagram follower and engagement analytics into Qala Observatory
- Reconcile Instagram Shop revenue in Dongo
- Surface Instagram growth metrics as Enzo enterprise KPIs
- Embed Instagram profile link in Heshima Linktree
- Route Instagram DMs and brand collab inquiries to ogun-messenger

---

### Facebook (`facebook`)

**Primary App:** `ayo`, `zuri`, `heshima`
**Integration Type:** Social media, pages, groups, and commerce connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:zuri.*`

**What It Is:** Facebook is a social networking platform with business pages, community groups, marketplace, and advertising tools widely used by service businesses and creators.

**How It Works in ogun OS:** Facebook integrates with `ayo` as a business page and group management channel. Facebook Page analytics are pulled into Qala. Facebook Group membership and engagement metrics are tracked as community health data. Facebook Marketplace listings can be synced from Zuri's product catalog. Facebook Shops revenue is reconciled in Dongo.

**Functions on the Platform:**
- Publish content to Facebook Page from Ayo's content interface
- Pull Facebook Page reach and engagement analytics into Qala Observatory
- Sync Facebook Marketplace / Shop listings from Zuri product catalog
- Reconcile Facebook Shop revenue in Dongo
- Track Facebook Group member count and activity in Qala
- Surface Facebook page performance in Enzo enterprise dashboard
- Embed Facebook page link in Heshima Linktree

---

### TikTok (`tiktok`)

**Primary App:** `ayo`, `zuri`, `dongo`
**Integration Type:** Short-form video publishing and commerce connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** TikTok is a short-form video platform with in-app commerce, creator monetization (TikTok Shop, Creator Fund, LIVE gifts), and a massive discovery algorithm.

**How It Works in ogun OS:** TikTok integrates with `ayo` as a video content publishing channel. TikTok analytics (followers, video views, likes, shares, profile visits, Creator Fund earnings) are pulled into Qala. TikTok Shop revenue is reconciled as a Dongo income stream. The OBSERVATORY_AGENT monitors TikTok revenue patterns as part of creator enterprise income tracking.

**Functions on the Platform:**
- Schedule and publish TikTok videos from Ayo's content interface (via TikTok API)
- Pull TikTok follower growth and video performance metrics into Qala Observatory
- Reconcile TikTok Shop and Creator Fund revenue in Dongo
- Track TikTok as an audience growth channel in Enzo enterprise dashboard
- Surface TikTok content performance as part of Content EHR calculations

---

### Snapchat (`snapchat`)

**Primary App:** `ayo`, `heshima`
**Integration Type:** Social media and audience connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Snapchat is a multimedia messaging and social media platform with creator monetization through Spotlight and Story ads — used by creators targeting younger demographics.

**How It Works in ogun OS:** Snapchat integrates with `ayo` as a social media channel for content scheduling and analytics tracking. Spotlight view counts and engagement metrics are pulled into Qala. Snapchat creator earnings are reconciled in Dongo.

**Functions on the Platform:**
- Track Snapchat follower and engagement metrics in Qala Observatory
- Reconcile Snapchat creator program earnings in Dongo
- Embed Snapchat profile in Heshima Linktree and Ayo spaces

---

### Bluesky (`bluesky`)

**Primary App:** `ayo`, `heshima`
**Integration Type:** Decentralized social media publishing connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Bluesky is a decentralized social media platform built on the AT Protocol, offering an open, user-owned alternative to centralized social networks.

**How It Works in ogun OS:** Bluesky integrates with `ayo` as a social publishing channel. Content can be cross-posted to Bluesky from Ayo's content creation interface. Follower count and post engagement metrics are tracked in Qala. The decentralized nature of Bluesky aligns with ogun OS's identity sovereignty model — the operator's Bluesky DID is registerable in Heshima as a verified decentralized identity handle.

**Functions on the Platform:**
- Publish and schedule posts to Bluesky from Ayo's content interface
- Pull Bluesky follower and engagement metrics into Qala Observatory
- Register Bluesky DID in Heshima as a verified decentralized identity
- Embed Bluesky profile in Heshima Linktree and Ayo spaces

---

### Threads (`threads`)

**Primary App:** `ayo`, `heshima`
**Integration Type:** Social media publishing connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Threads is Meta's text-based social media platform tightly integrated with Instagram, used for conversation and thought leadership content.

**How It Works in ogun OS:** Threads integrates with `ayo` as a text content channel. Threads analytics (followers, impressions, replies) are pulled into Qala. Content can be drafted in Ayo and cross-posted to Threads.

**Functions on the Platform:**
- Publish content to Threads from Ayo's content interface
- Track Threads engagement metrics in Qala Observatory
- Embed Threads profile in Heshima Linktree

---

### Pinterest (`pinterest`)

**Primary App:** `ayo`, `zuri`
**Integration Type:** Visual content and social commerce connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Pinterest is a visual discovery and social commerce platform used by creators and small businesses in design, food, fashion, home, and craft niches.

**How It Works in ogun OS:** Pinterest integrates with `ayo` as a visual content publishing channel. Pinterest analytics (monthly views, pin impressions, profile followers, click-throughs) are tracked in Qala. Pinterest Shop product pins can be synced from Zuri's product catalog. Pinterest referral traffic to linked Zuri stores or Ayo spaces is tracked as acquisition data.

**Functions on the Platform:**
- Schedule and publish Pins from Ayo's visual content interface
- Sync Zuri product catalog to Pinterest Shop for shoppable pins
- Pull Pinterest analytics into Qala Observatory
- Track Pinterest as a referral traffic source for Zuri stores

---

### Nextdoor (`nextdoor`)

**Primary App:** `ayo`, `kogi`
**Integration Type:** Local community and business discovery connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Nextdoor is a neighborhood social network that allows local businesses and service providers to reach nearby customers through local recommendations, business profiles, and community posts.

**How It Works in ogun OS:** Nextdoor integrates with `kogi` as a local lead generation channel for service-based enterprises (contractors, tradespeople, home service providers). Inbound Nextdoor inquiries and recommendation notifications are routed to ogun-messenger and can be converted to Kogi pipeline entries.

**Functions on the Platform:**
- Route Nextdoor business inquiries to ogun-messenger
- Convert Nextdoor leads to Kogi pipeline entries
- Track Nextdoor as a client acquisition channel in Qala

---

### LinkedIn (`linkedin`)

**Primary App:** `ayo`, `heshima`, `kogi`
**Integration Type:** Professional network and B2B lead generation connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:kogi.*`

**What It Is:** LinkedIn is a professional networking platform used by consultants, coaches, founders, and B2B service providers for thought leadership, client prospecting, and recruiting.

**How It Works in ogun OS:** LinkedIn integrates with `ayo` as a professional content publishing channel and with `kogi` as a B2B lead generation channel. Posts can be scheduled from Ayo. LinkedIn analytics (followers, post impressions, connection requests) are tracked in Qala. LinkedIn message inquiries are routed to ogun-messenger. The ACQUISITION_AGENT can monitor LinkedIn connection and engagement metrics at OBSERVE authority.

**Functions on the Platform:**
- Publish and schedule LinkedIn posts from Ayo's content interface
- Pull LinkedIn follower and engagement metrics into Qala Observatory
- Route LinkedIn DMs to ogun-messenger
- Track LinkedIn as a B2B client acquisition channel in Kogi's pipeline analytics
- Embed LinkedIn profile in Heshima Linktree and Ayo digital spaces
- Enable Acquisition Agent to monitor engagement signals at OBSERVE

---

### Mastodon (`mastodon`)

**Primary App:** `ayo`, `heshima`
**Integration Type:** Decentralized social media publishing connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Mastodon is an open-source, decentralized social networking platform that forms part of the Fediverse, offering an alternative to corporate social media.

**How It Works in ogun OS:** Mastodon integrates with `ayo` as a decentralized social publishing channel. The operator's Mastodon handle can be registered in Heshima as a Fediverse identity. Content can be cross-posted from Ayo's publishing interface.

**Functions on the Platform:**
- Publish content to Mastodon from Ayo's content interface
- Register Mastodon handle in Heshima as a verified Fediverse identity
- Track Mastodon follower and engagement metrics in Qala

---

### YouTube (`youtube`)

**Primary App:** `ayo`, `shango`, `dongo`
**Integration Type:** Video content publishing and monetization connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:shango.*`

**What It Is:** YouTube is the world's largest video platform with comprehensive creator monetization tools including AdSense, channel memberships, Super Chat, Super Thanks, and YouTube Shopping.

**How It Works in ogun OS:** YouTube integrates with `ayo` as a primary video content production and distribution channel and with `shango` as a content factory output. Videos produced through Shango's content pipeline are published to YouTube. YouTube Studio analytics (views, subscribers, watch time, revenue from ads, memberships, and shopping) are pulled comprehensively into Qala.

YouTube AdSense earnings, channel membership revenue, and YouTube Shopping commissions are reconciled as separate income streams in Dongo. The OBSERVATORY_AGENT tracks YouTube channel growth as a core creator enterprise KPI.

Castmagic integration (if enabled) automatically processes new YouTube uploads to generate transcripts, chapters, and repurposed content assets.

**Functions on the Platform:**
- Publish videos to YouTube directly from Shango's content production pipeline or Ayo's content interface
- Pull comprehensive YouTube Studio analytics (views, watch time, subscriber growth, revenue) into Qala Observatory
- Reconcile YouTube AdSense, membership, and Shopping revenue as attributed income streams in Dongo
- Track YouTube as a core audience and revenue channel in Enzo enterprise dashboard
- Feed Content EHR calculations with YouTube revenue data
- Surface YouTube revenue in Dongo's financial health score
- Enable Castmagic integration to auto-process new YouTube video uploads

---

### Twitch (`twitch`)

**Primary App:** `ayo`, `dongo`, `shango`
**Integration Type:** Live streaming and creator monetization connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Twitch is the leading live streaming platform for gaming, creative content, and "just chatting" streams, with monetization through subscriptions, Bits, ad revenue, and channel points.

**How It Works in ogun OS:** Twitch integrates with `ayo` as a live content publishing channel. Twitch stream schedule is synced to Misimu's calendar. Twitch analytics (concurrent viewers, followers, subscription count, Bits received) are pulled into Qala. Twitch affiliate and partner revenue is reconciled in Dongo.

**Functions on the Platform:**
- Sync Twitch stream schedule to Misimu calendar
- Pull Twitch viewership and follower analytics into Qala Observatory
- Reconcile Twitch subscription, Bits, and ad revenue in Dongo
- Track Twitch as an audience growth channel in Enzo enterprise dashboard
- Embed Twitch channel link in Ayo spaces and Heshima Linktree

---

### Buffer (`buffer`)

**Primary App:** `ayo`
**Integration Type:** Social media scheduling and analytics connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Buffer is a social media management tool for scheduling posts across multiple platforms and analyzing cross-channel content performance.

**How It Works in ogun OS:** Buffer integrates with `ayo` as a cross-channel content scheduling layer. Content drafted in Ayo can be queued to Buffer for multi-platform publishing. Buffer analytics (cross-channel engagement summary, best-performing posts) are pulled into Qala as content performance data.

**Functions on the Platform:**
- Queue content from Ayo's content interface to Buffer for multi-platform scheduling
- Pull cross-channel analytics from Buffer into Qala Observatory
- Track social media publishing consistency as a content production metric

---

## 7. Professional Networks & Forums

---

### Stack Overflow (`stackoverflow`)

**Primary App:** `akeel`, `ayo`, `heshima`
**Integration Type:** Knowledge community and developer profile connector
**Capability Required:** `network.outbound`, `ipc.write:akeel.*`

**What It Is:** Stack Overflow is the world's largest developer question-and-answer community, used by software developers for technical reference and community engagement.

**How It Works in ogun OS:** Stack Overflow integrates with `akeel` as a knowledge source connector. Saved questions, answers, and bookmarks from Stack Overflow can be synced into Akeel's knowledge base as technical reference material. The operator's Stack Overflow reputation score and badges are registerable in Heshima as professional credentials.

**Functions on the Platform:**
- Sync Stack Overflow bookmarks and saved answers into Akeel knowledge base
- Register Stack Overflow reputation as a professional credential in Heshima
- Embed Stack Overflow profile in Heshima Linktree and Ayo spaces
- Track contribution volume as a professional activity metric in Qala

---

### Quora (`quora`)

**Primary App:** `ayo`, `akeel`
**Integration Type:** Thought leadership and content distribution connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Quora is a question-and-answer platform used by professionals for thought leadership and audience building through expert answers.

**How It Works in ogun OS:** Quora integrates with `ayo` as a thought leadership content channel. Published Quora answers are tracked as content artifacts. Answer views and follower metrics are pulled into Qala as audience reach data. High-performing answers are indexed in Akeel.

**Functions on the Platform:**
- Track Quora answer views and follower metrics in Qala Observatory
- Index high-value published Quora answers in Akeel knowledge base
- Embed Quora profile in Heshima Linktree

---

### Reddit (`reddit`)

**Primary App:** `ayo`, `kogi`
**Integration Type:** Community monitoring and content distribution connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Reddit is a network of communities (subreddits) used for content sharing, discussion, community building, and marketing — particularly for tech, finance, and niche interest operators.

**How It Works in ogun OS:** Reddit integrates with `ayo` as a community monitoring and content channel. Relevant subreddit mentions or threads can be tracked as market intelligence signals fed to Qala. The ACQUISITION_AGENT can monitor subreddits relevant to the operator's ICP at OBSERVE authority for inbound lead signals.

**Functions on the Platform:**
- Monitor relevant subreddits for brand mentions and inbound signals (OBSERVE authority)
- Feed subreddit engagement data to Qala as market intelligence
- Track Reddit as a content distribution channel in Qala

---

## 8. Publishing & Newsletters

---

### Substack (`substack`)

**Primary App:** `ayo`, `dongo`, `shango`
**Integration Type:** Newsletter publishing and subscription revenue connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `ipc.write:shango.*`

**What It Is:** Substack is a platform for independent writers and creators to publish newsletters and build subscription-based businesses with paying subscribers.

**How It Works in ogun OS:** Substack integrates with `ayo` as a newsletter publishing channel and with `shango` as a content production pipeline output. Newsletter drafts created in Shango's content factory can be published directly to Substack. Substack analytics (subscribers, open rates, paid subscriber count, revenue) are pulled into Qala.

Substack subscription revenue is reconciled as a recurring income stream in Dongo — an MRR component tracked in the Enzo enterprise dashboard. The OBSERVATORY_AGENT monitors subscriber growth and churn as newsletter health KPIs.

**Functions on the Platform:**
- Publish newsletters to Substack from Shango's content production pipeline or Ayo's content interface
- Pull Substack subscriber, open rate, and revenue metrics into Qala Observatory
- Reconcile Substack subscription revenue as an MRR component in Dongo
- Track Substack growth as a creator enterprise KPI in Enzo
- Display Substack publish link in Heshima Linktree and Ayo spaces

---

### Medium (`medium`)

**Primary App:** `ayo`, `shango`, `akeel`
**Integration Type:** Article publishing and audience connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Medium is a publishing platform used by writers, thinkers, and professionals for long-form articles and thought leadership content with a built-in audience.

**How It Works in ogun OS:** Medium integrates with `ayo` as a long-form content publishing channel. Articles produced in Shango's content pipeline can be formatted and published to Medium. Medium Partner Program earnings are reconciled in Dongo. Published articles are indexed in Akeel as knowledge artifacts.

**Functions on the Platform:**
- Publish articles to Medium from Shango's content pipeline or Ayo's interface
- Reconcile Medium Partner Program earnings in Dongo
- Index published Medium articles in Akeel's knowledge base
- Track Medium follower and article clap metrics in Qala Observatory
- Embed Medium profile in Heshima Linktree

---

### Ghost (`ghost`)

**Primary App:** `ayo`, `dongo`, `shango`
**Integration Type:** Independent publishing and membership platform connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Ghost is an open-source publishing platform used by independent media businesses and creators for running subscription newsletters and content sites with full ownership.

**How It Works in ogun OS:** Ghost integrates with `ayo` as a self-hosted publishing channel and with `dongo` as a subscription revenue source. Ghost membership revenue is reconciled as an MRR component. Ghost subscriber counts and email engagement metrics are tracked in Qala.

**Functions on the Platform:**
- Pull Ghost subscriber and engagement metrics into Qala Observatory
- Reconcile Ghost membership revenue as an MRR component in Dongo
- Track Ghost site as an external digital space in Ayo
- Monitor Ghost subscriber growth as a creator enterprise KPI

---

### Overleaf (`overleaf`)

**Primary App:** `shango`, `akeel`
**Integration Type:** Academic and technical document authoring connector
**Capability Required:** `network.outbound`, `ipc.write:shango.*`

**What It Is:** Overleaf is a cloud-based LaTeX editor used by researchers, academics, and technical writers for producing scientific papers, reports, and technical documentation.

**How It Works in ogun OS:** Overleaf integrates with `shango` as a specialized technical document production tool and with `akeel` for document archiving. Completed Overleaf documents are exported as artifacts and stored in the VFS under `artifact://[enterprise-id]/documents/`.

**Functions on the Platform:**
- Export Overleaf documents as registered artifacts in the VFS
- Index completed Overleaf documents in Akeel's knowledge base
- Track document production in Shango's production metrics

---

## 9. Creator Monetization & Commerce

---

### LTK / LikeToKnowIt (`ltk`)

**Primary App:** `zuri`, `ayo`, `dongo`
**Integration Type:** Affiliate commerce and creator shopping connector
**Capability Required:** `network.outbound`, `ipc.write:zuri.*`, `ipc.write:dongo.*`

**What It Is:** LTK (formerly LikeToKnowIt/rewardStyle) is a creator shopping platform that allows lifestyle and fashion creators to curate shoppable product lists and earn affiliate commissions.

**How It Works in ogun OS:** LTK integrates with `zuri` as an affiliate commerce channel. LTK commission earnings are reconciled in `dongo` as an affiliate income stream. LTK shop link is embedded in `heshima` Linktree and `ayo` spaces. The OBSERVATORY_AGENT monitors LTK earnings trends and correlates them with content publishing activity as part of the creator enterprise's passive income ratio tracking.

**Functions on the Platform:**
- Reconcile LTK affiliate commissions as an attributed income stream in Dongo
- Display LTK shop link in Heshima Linktree and Ayo digital spaces
- Track LTK earnings as a passive income component in Enzo enterprise dashboard
- Monitor LTK commission trends in Qala Observatory
- Feed LTK data to passive income ratio calculations

---

### ShopMy (`shopmy`)

**Primary App:** `zuri`, `ayo`, `dongo`
**Integration Type:** Affiliate storefront and creator commerce connector
**Capability Required:** `network.outbound`, `ipc.write:zuri.*`

**What It Is:** ShopMy is a creator monetization platform that allows creators to build personalized storefronts with affiliate product recommendations and earn commissions from purchases.

**How It Works in ogun OS:** Same architecture as LTK. ShopMy affiliate commissions are reconciled in Dongo as a passive income stream. The ShopMy storefront link is embedded in Heshima Linktree and Ayo spaces. Commission trends are tracked in Qala Observatory.

**Functions on the Platform:**
- Reconcile ShopMy commissions as attributed income in Dongo
- Display ShopMy storefront link in Heshima Linktree and Ayo spaces
- Track ShopMy earnings as passive income in Enzo enterprise dashboard

---

### Etsy (`etsy`)

**Primary App:** `zuri`, `dongo`, `shango`
**Integration Type:** Handmade and digital goods marketplace connector
**Capability Required:** `network.outbound`, `ipc.write:zuri.*`, `financial.write`

**What It Is:** Etsy is a marketplace for handmade, vintage, and digital products — used by creators and makers to sell products with a built-in buyer audience.

**How It Works in ogun OS:** Etsy integrates with `zuri` as an external marketplace channel. Etsy shop orders are synced to Zuri's order management registry. Etsy revenue is reconciled as an attributed income stream in Dongo. Etsy product listings can be managed through Zuri's product catalog interface with cross-publishing to the Etsy shop.

**Functions on the Platform:**
- Sync Etsy shop orders into Zuri's order management registry
- Reconcile Etsy revenue as an attributed income stream in Dongo
- Manage Etsy product listings through Zuri's catalog interface
- Pull Etsy shop analytics (views, favorites, conversion rate) into Qala Observatory
- Track Etsy shop health as an Enzo enterprise KPI

---

### Shopify (`shopify`)

**Primary App:** `zuri`, `dongo`, `shango`
**Integration Type:** E-commerce platform connector
**Capability Required:** `network.outbound`, `ipc.write:zuri.*`, `financial.write`

**What It Is:** Shopify is an all-in-one e-commerce platform used by product businesses and digital goods sellers to build and run online stores with full inventory, shipping, and payments management.

**How It Works in ogun OS:** Shopify integrates with `zuri` as an external e-commerce storefront channel. Shopify orders are synced into Zuri's order management registry. Shopify revenue (including product sales, subscriptions, and app charges) is reconciled in Dongo. Shopify inventory levels feed Shango's inventory management system for physical product businesses.

**Functions on the Platform:**
- Sync Shopify orders into Zuri's order management registry
- Reconcile all Shopify revenue streams in Dongo
- Feed Shopify inventory levels to Shango's inventory management
- Pull Shopify store analytics (GMV, conversion rate, average order value) into Qala Observatory
- Track Shopify as a primary commerce channel in Enzo enterprise dashboard
- Support the Bookkeeping Agent in reconciling Shopify transactions

---

### AspireIQ (`aspireiq`)

**Primary App:** `kogi`, `dongo`, `ume`
**Integration Type:** Brand partnership and influencer management connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** AspireIQ is an influencer marketing platform that connects creators with brands for paid partnerships, affiliate campaigns, and content collaborations.

**How It Works in ogun OS:** AspireIQ integrates with `kogi` as a brand deal pipeline channel. Inbound partnership opportunities from AspireIQ are routed to Kogi's pipeline as new engagement proposals. Campaign deliverables are tracked in Moto. Partnership revenue is reconciled in Dongo with proper attribution.

**Functions on the Platform:**
- Route AspireIQ partnership opportunities to Kogi as pipeline entries
- Track campaign deliverables in Moto's project management system
- Reconcile brand partnership revenue in Dongo
- Store partnership contracts in Ume's contract management system
- Track brand deal pipeline value as EPV in Enzo enterprise dashboard

---

### CreatorIQ (`createiq`)

**Primary App:** `kogi`, `dongo`, `ume`
**Integration Type:** Creator brand partnership connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** CreatorIQ is an enterprise influencer marketing platform used by major brands to manage creator partnerships, content approvals, and campaign analytics.

**How It Works in ogun OS:** Same architecture as AspireIQ. CreatorIQ campaign briefs are routed to Kogi as engagement entries. Campaign deliverables are tracked in Moto. Partnership payments are reconciled in Dongo.

**Functions on the Platform:**
- Route CreatorIQ campaign opportunities to Kogi
- Track deliverables in Moto
- Reconcile campaign revenue in Dongo

---

### OnlyFans (`onlyfans`)

**Primary App:** `ayo`, `dongo`, `shango`
**Integration Type:** Creator subscription and content monetization connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`, `financial.read`

**What It Is:** OnlyFans is a content subscription platform where creators monetize content through monthly subscriptions, pay-per-view posts, and tips — used across fitness, cooking, music, education, and other niches.

**How It Works in ogun OS:** OnlyFans integrates with `dongo` as a subscription income source. OnlyFans subscription revenue, tips, and PPV earnings are reconciled as attributed income streams. The Enzo enterprise dashboard tracks OnlyFans MRR as part of the creator enterprise's recurring revenue base. Content produced in Shango's content pipeline feeds OnlyFans publishing.

**Functions on the Platform:**
- Reconcile OnlyFans subscription revenue, tips, and PPV earnings in Dongo as attributed income streams
- Track OnlyFans MRR as part of creator enterprise MRR in Enzo
- Monitor subscriber count and churn in Qala Observatory
- Feed OnlyFans passive income to passive income ratio calculations

---

## 10. Freelance & Gig Marketplaces

---

### Upwork (`upwork`)

**Primary App:** `kogi`, `dongo`, `ume`
**Integration Type:** Freelance marketplace and contract management connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Upwork is the world's largest freelance marketplace, connecting businesses with independent professionals for project-based and long-term contract work.

**How It Works in ogun OS:** Upwork integrates with `kogi` as a primary pipeline channel for freelance operators. Active Upwork contracts are surfaced in Kogi's engagement management system. Upwork contracts are stored in Ume's contract lifecycle management. Upwork earnings and hourly logs are reconciled with Dongo's income management and contribute to EHR calculations.

The PRICING_AGENT monitors Upwork hourly rate relative to the operator's declared EHR floor and suggests profile rate adjustments at RECOMMEND authority.

**Functions on the Platform:**
- Sync active Upwork contracts to Kogi's engagement registry
- Store Upwork contract documents in Ume's contract management
- Reconcile Upwork earnings as attributed income in Dongo
- Include Upwork hourly rates and billed hours in EHR calculations
- Enable Pricing Agent to monitor and recommend Upwork profile rate adjustments
- Feed Upwork pipeline proposals to EPV calculations in Enzo
- Track Upwork client concentration risk in Enzo enterprise dashboard

---

### Fiverr (`fiverr`)

**Primary App:** `kogi`, `dongo`, `zuri`
**Integration Type:** Gig marketplace and digital service connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Fiverr is a freelance services marketplace known for packaged "gig" offerings, used by designers, writers, marketers, developers, and voice-over artists for digital service sales.

**How It Works in ogun OS:** Fiverr integrates with `kogi` as an inbound order pipeline. New Fiverr orders are converted to Kogi engagement entries. Fiverr gig offerings mirror Shango product offerings — the Productization Agent can identify when a service pattern would benefit from a packaged Fiverr gig. Fiverr revenue is reconciled in Dongo.

**Functions on the Platform:**
- Convert new Fiverr orders to Kogi engagement entries
- Reconcile Fiverr revenue as attributed income in Dongo
- Include Fiverr order value in EPV calculations
- Enable Productization Agent to flag productizable service patterns via Fiverr performance data
- Track Fiverr as a client acquisition channel in Kogi's pipeline analytics

---

### Solo / Solo App (`solo`)

**Primary App:** `kogi`, `dongo`, `heshima`
**Integration Type:** Freelancer operations and invoicing connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Solo (and related "solo app" services) are freelance management platforms offering invoicing, contract generation, expense tracking, and tax tools for independent workers.

**How It Works in ogun OS:** Solo integrates with `kogi` for engagement and invoicing management and with `dongo` for financial reconciliation. Invoices generated in Solo are tracked in Dongo's accounts receivable. Payment receipts are reconciled as income records.

**Functions on the Platform:**
- Sync Solo invoices to Dongo's accounts receivable
- Reconcile Solo payment receipts as attributed income
- Import Solo contracts into Ume's contract management

---

### TaskRabbit (`taskrabbit`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** On-demand task marketplace connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** TaskRabbit is an on-demand marketplace for local task services (furniture assembly, moving, cleaning, handyman work) that connects Taskers with customers.

**How It Works in ogun OS:** TaskRabbit integrates with `kogi` as a job pipeline source. Completed TaskRabbit jobs are logged as Kogi engagement records. TaskRabbit earnings are reconciled in Dongo. Job location data and repeat customer patterns are tracked in Kogi's client management.

**Functions on the Platform:**
- Log TaskRabbit jobs as Kogi engagement records
- Reconcile TaskRabbit earnings as attributed income in Dongo
- Track TaskRabbit as a client acquisition channel
- Include TaskRabbit earnings in EHR calculations

---

### Thumbtack (`thumbtack`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Local service marketplace connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Thumbtack is a marketplace for local professional services (plumbers, electricians, personal trainers, photographers) connecting customers with local providers.

**How It Works in ogun OS:** Thumbtack integrates with `kogi` as a lead generation and job pipeline channel. Thumbtack quote requests are converted to Kogi pipeline entries. Won jobs become active engagement records. Thumbtack revenue reconciles in Dongo.

**Functions on the Platform:**
- Convert Thumbtack quote requests to Kogi pipeline leads
- Create active Kogi engagement records for won Thumbtack jobs
- Reconcile Thumbtack earnings in Dongo
- Track Thumbtack as an acquisition channel with win/loss analytics in Kogi

---

### Angie's List / Angi (`angieslist`)

**Primary App:** `kogi`, `dongo`, `heshima`
**Integration Type:** Home services marketplace connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Angi (formerly Angie's List) is a marketplace for home improvement and service professionals connecting homeowners with vetted contractors and service providers.

**How It Works in ogun OS:** Angi integrates with `kogi` as a lead and job pipeline channel. New Angi leads are routed as Kogi pipeline entries. Job completion triggers engagement status updates. Reviews and ratings from Angi are tracked in Heshima's reputation management system.

**Functions on the Platform:**
- Route Angi leads to Kogi as pipeline entries
- Update engagement lifecycle on Angi job completion
- Sync Angi reviews and ratings to Heshima reputation management
- Track Angi as a client acquisition channel in Kogi analytics

---

### GigSmart (`gigsmart`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** On-demand workforce connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** GigSmart is an on-demand staffing platform for shift-based gig work in warehousing, events, hospitality, and labor.

**How It Works in ogun OS:** GigSmart integrates with `kogi` for shift tracking and with `dongo` for earnings reconciliation. Completed GigSmart shifts are logged as engagement records. Shift earnings reconcile as income in Dongo.

**Functions on the Platform:**
- Log GigSmart shifts as Kogi engagement records
- Reconcile GigSmart earnings in Dongo
- Include shift earnings in EHR calculations

---

### Instawork (`instawork`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Hospitality and event staffing connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Instawork is an on-demand staffing platform for hospitality, food service, and event gig workers.

**How It Works in ogun OS:** Same architecture as GigSmart. Instawork shifts log as Kogi engagement records and earnings reconcile in Dongo.

**Functions on the Platform:**
- Log Instawork shifts as Kogi engagement records
- Reconcile Instawork earnings in Dongo

---

### Qwick (`qwick`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Food and hospitality staffing connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Qwick is a gig platform for culinary and hospitality professionals connecting restaurant/catering staff with shift-based work opportunities.

**How It Works in ogun OS:** Qwick shifts integrate as Kogi engagement records with Dongo income reconciliation.

**Functions on the Platform:**
- Log Qwick shifts as Kogi engagement records
- Reconcile Qwick earnings in Dongo

---

### Wonolo (`wonolo`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** On-demand workforce connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Wonolo is an on-demand staffing platform for warehouse, logistics, and light industrial gig work.

**How It Works in ogun OS:** Same architecture as GigSmart and Instawork.

**Functions on the Platform:**
- Log Wonolo shifts as Kogi engagement records
- Reconcile Wonolo earnings in Dongo

---

### Poplin (`poplin`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** On-demand laundry service connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Poplin (formerly Laundry Care) is an on-demand platform for independent laundry service providers.

**How It Works in ogun OS:** Poplin orders integrate as Kogi engagement records. Poplin earnings reconcile in Dongo.

**Functions on the Platform:**
- Log Poplin jobs as Kogi engagement records
- Reconcile Poplin earnings in Dongo

---

## 11. On-Demand & Service Marketplaces

---

### Uber (`uber`)

**Primary App:** `kogi`, `dongo`, `zamani`
**Integration Type:** Rideshare and gig income connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Uber is a rideshare platform used by independent drivers (Uber Eats drivers, UberX, etc.) as a primary or supplementary income source.

**How It Works in ogun OS:** Uber integrates with `dongo` as a gig income source. Weekly Uber earnings statements are pulled and reconciled as attributed income in Dongo. Uber miles driven are tracked for tax deduction purposes. Vehicle costs attributable to Uber driving (fuel, maintenance, depreciation) are tracked in Zamani's asset and expense management.

**Functions on the Platform:**
- Reconcile weekly Uber earnings as attributed income in Dongo
- Track Uber-related mileage for tax deduction documentation
- Monitor vehicle expense allocation for Uber driving in Zamani
- Include Uber income in EHR calculations

---

### Instacart (`instacart`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Gig grocery delivery income connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Instacart is a grocery delivery platform where independent shoppers earn income fulfilling customer orders.

**How It Works in ogun OS:** Instacart earnings reconcile in Dongo as gig income. Mileage tracking integrates with tax deduction documentation.

**Functions on the Platform:**
- Reconcile Instacart earnings in Dongo
- Track delivery mileage for tax deduction purposes

---

### Grubhub (`grubhub`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Food delivery gig income connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Grubhub is a food delivery platform where independent couriers earn income delivering restaurant orders.

**How It Works in ogun OS:** Grubhub earnings reconcile in Dongo. Mileage and vehicle expense tracking supports tax deduction management.

**Functions on the Platform:**
- Reconcile Grubhub earnings in Dongo
- Track delivery mileage for tax deductions

---

### DoorDash (`doordash`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Food delivery gig income connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** DoorDash is the largest US food delivery platform with independent courier (Dasher) gig opportunities.

**How It Works in ogun OS:** Same as Grubhub architecture.

**Functions on the Platform:**
- Reconcile DoorDash earnings in Dongo
- Track delivery mileage for tax deductions
- Include DoorDash income in EHR calculations

---

## 12. Field Service & Trade Tools

---

### Jobber (`jobber`)

**Primary App:** `kogi`, `dongo`, `ume`, `moto`
**Integration Type:** Field service management connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Jobber is a field service management platform for home service businesses (landscaping, cleaning, HVAC, plumbing) with job scheduling, quoting, invoicing, and client management.

**How It Works in ogun OS:** Jobber integrates deeply with `kogi` as the primary operational system for trades and field service operators. Jobber jobs are synced as Kogi engagement records. Jobber quotes map to Kogi pipeline proposals. Jobber invoices reconcile in Dongo. Jobber's client records sync with Kogi's client management and ogun-contacts.

**Functions on the Platform:**
- Sync Jobber jobs as Kogi engagement records with full lifecycle tracking
- Map Jobber quotes to Kogi pipeline proposals for EPV tracking
- Reconcile Jobber invoices in Dongo's accounts receivable
- Sync Jobber clients to ogun-contacts and Kogi client management
- Pull Jobber job completion metrics into Qala Observatory
- Track Jobber field technician scheduling in Misimu calendar
- Enable Pricing Agent to analyze Jobber service pricing vs. EHR floor

---

### Housecall Pro (`housecallpro`)

**Primary App:** `kogi`, `dongo`, `ume`
**Integration Type:** Field service management connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Housecall Pro is a field service management platform for home services businesses with scheduling, dispatching, invoicing, and customer management.

**How It Works in ogun OS:** Identical architecture to Jobber. Housecall Pro jobs sync to Kogi, invoices reconcile in Dongo, clients sync to ogun-contacts.

**Functions on the Platform:**
- Sync Housecall Pro jobs as Kogi engagement records
- Reconcile invoices in Dongo
- Sync client records to ogun-contacts
- Pull scheduling to Misimu calendar

---

### Vagaro (`vagaro`)

**Primary App:** `kogi`, `dongo`, `misimu`
**Integration Type:** Salon, spa, and wellness booking connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`, `financial.read`

**What It Is:** Vagaro is an appointment and business management platform for salons, spas, massage therapists, and personal trainers.

**How It Works in ogun OS:** Vagaro appointments sync to `misimu`'s calendar. Booking revenue reconciles in Dongo. Vagaro client records sync to ogun-contacts. The Pricing Agent monitors average Vagaro service revenue vs. EHR floor.

**Functions on the Platform:**
- Sync Vagaro appointments to Misimu calendar
- Reconcile Vagaro booking revenue in Dongo
- Sync Vagaro clients to ogun-contacts
- Enable Pricing Agent to analyze service pricing vs. EHR floor
- Track booking fill rate and no-show rate in Qala Observatory

---

## 13. Crowdfunding & Community Funding

---

### GoFundMe (`gofundme`)

**Primary App:** `dongo`, `ayo`
**Integration Type:** Donation and campaign fundraising connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** GoFundMe is a personal and business crowdfunding platform used for fundraising campaigns for causes, projects, and emergencies.

**How It Works in ogun OS:** GoFundMe integrates with `dongo` as a campaign fundraising income source. Active campaign donations are tracked as income records with appropriate attribution. Campaign progress is surfaced in Ayo as a community engagement metric.

**Functions on the Platform:**
- Track GoFundMe campaign donation income in Dongo
- Display active campaign progress in Ayo community spaces
- Monitor fundraising milestone achievement in Qala

---

### Indiegogo (`indiegogo`)

**Primary App:** `dongo`, `zuri`, `ayo`
**Integration Type:** Crowdfunding and product launch connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Indiegogo is a crowdfunding platform used for product launches, creative projects, and business campaigns — with both all-or-nothing and flexible funding models.

**How It Works in ogun OS:** Indiegogo campaign funding is tracked in `dongo` as project pre-sale revenue. Campaign analytics (backer count, funding progress, referral sources) are pulled into Qala. Indiegogo connects to `shango` for production planning when a campaign funds successfully — triggering the production pipeline for backer fulfillment.

**Functions on the Platform:**
- Track Indiegogo campaign funding as pre-sale revenue in Dongo
- Pull campaign metrics (backers, funding percentage) into Qala Observatory
- Trigger Shango production planning upon campaign success
- Display active campaign in Ayo spaces and Heshima profiles

---

### Kickstarter (`kickstarter`)

**Primary App:** `dongo`, `shango`, `zuri`, `ayo`
**Integration Type:** Creative crowdfunding connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Kickstarter is the world's leading crowdfunding platform for creative projects — games, films, books, hardware, and design products.

**How It Works in ogun OS:** Same architecture as Indiegogo. Kickstarter backers and funding progress track in Qala. Successful campaign funding triggers Shango production planning. Revenue reconciles in Dongo.

**Functions on the Platform:**
- Track Kickstarter campaign funding in Dongo
- Trigger Shango production pipeline on campaign success
- Pull campaign metrics into Qala Observatory
- Display campaign in Ayo spaces

---

### Mightycause (`mightycause`)

**Primary App:** `dongo`, `ayo`
**Integration Type:** Nonprofit and cause-based fundraising connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Mightycause is a fundraising platform for nonprofits and cause-based campaigns.

**How It Works in ogun OS:** Mightycause donation income tracks in Dongo. Campaign progress displays in Ayo for community-facing enterprises.

**Functions on the Platform:**
- Track Mightycause donation income in Dongo
- Display campaign progress in Ayo community spaces

---

### Kiva (`kiva`)

**Primary App:** `dongo`, `zamani`, `igi`
**Integration Type:** Microfinance and impact investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Kiva is a microfinance platform where lenders can make small loans to entrepreneurs and borrowers globally, often used by mission-driven investors and impact operators.

**How It Works in ogun OS:** Kiva lending activity integrates with `igi` as an impact investment portfolio item. Active Kiva loans are tracked as portfolio positions. Repayments are recorded as income in Dongo. Kiva activity is tracked in the investment enterprise's KPI dashboard.

**Functions on the Platform:**
- Track active Kiva loans as portfolio positions in Igi
- Record Kiva repayments as attributed income in Dongo
- Display Kiva impact metrics in the investment enterprise dashboard

---

## 14. Investment & Equity Crowdfunding

---

### StartEngine (`startengine`)

**Primary App:** `igi`, `dongo`, `didara`, `zamani`
**Integration Type:** Equity crowdfunding investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** StartEngine is a Regulation A+ and Regulation CF equity crowdfunding platform where both operators raising capital and investors participate.

**How It Works in ogun OS:** For investors, StartEngine holdings are tracked as portfolio positions in `igi`. Investment amounts are recorded in Dongo. For founders raising capital on StartEngine, the campaign tracks in the Enzo founder enterprise dashboard with investor count and raise progress as KPIs. Cap table implications are managed in Ume.

**Functions on the Platform:**
- Track StartEngine investment positions in Igi portfolio management
- Record investment capital deployed in Dongo
- Track cap table changes from StartEngine raises in Ume
- Monitor raise progress as a founder enterprise KPI in Enzo
- Record StartEngine equity positions in Zamani estate management

---

### Republic (`republic`)

**Primary App:** `igi`, `dongo`, `ume`
**Integration Type:** Equity and alternative investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Republic is an equity crowdfunding platform offering startup investments, crypto projects, and real estate opportunities to non-accredited investors.

**How It Works in ogun OS:** Republic investments track as portfolio positions in `igi`. Investment capital deploys as Dongo outflows. For founders raising, Republic campaigns track in Enzo with cap table management in Ume.

**Functions on the Platform:**
- Track Republic investment positions in Igi
- Record investment transactions in Dongo
- Manage cap table for Republic raise in Ume

---

### CircleUp (`circleup`)

**Primary App:** `igi`, `dongo`
**Integration Type:** Consumer goods investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** CircleUp is an equity investment platform focused on consumer goods and retail businesses.

**How It Works in ogun OS:** CircleUp investment positions track in `igi`. Investment capital records in Dongo.

**Functions on the Platform:**
- Track CircleUp positions in Igi portfolio management
- Record CircleUp investment activity in Dongo

---

### Climatize (`climatize`)

**Primary App:** `igi`, `dongo`
**Integration Type:** Climate impact investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Climatize is an investment platform for clean energy and climate-focused projects.

**How It Works in ogun OS:** Climatize holdings track as impact investment portfolio items in `igi`.

**Functions on the Platform:**
- Track Climatize investments in Igi
- Record returns and income in Dongo

---

### EquityZen (`equityzen`)

**Primary App:** `igi`, `dongo`, `zamani`
**Integration Type:** Pre-IPO secondary market connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** EquityZen is a secondary market platform for buying and selling shares in pre-IPO private companies.

**How It Works in ogun OS:** EquityZen holdings track as alternative investment positions in `igi`. Holdings are included in Zamani's equity and securities management.

**Functions on the Platform:**
- Track EquityZen pre-IPO holdings in Igi
- Include positions in Zamani equity management
- Record transactions in Dongo

---

### OurCrowd (`ourcrowd`)

**Primary App:** `igi`, `dongo`
**Integration Type:** Venture investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** OurCrowd is an equity crowdfunding platform for accredited investors to invest in early-stage startups alongside venture capitalists.

**How It Works in ogun OS:** OurCrowd portfolio companies track as venture investment positions in `igi`. Investment returns and distributions record in Dongo.

**Functions on the Platform:**
- Track OurCrowd portfolio positions in Igi
- Record OurCrowd investment returns in Dongo

---

### Wefunder (`wefunder`)

**Primary App:** `igi`, `dongo`, `ume`
**Integration Type:** Community round fundraising and investment connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Wefunder is a Regulation CF equity crowdfunding platform for startups raising from their community.

**How It Works in ogun OS:** For investors, Wefunder positions track in `igi`. For founders, Wefunder campaigns track in Enzo with cap table management in Ume.

**Functions on the Platform:**
- Track Wefunder investment positions in Igi
- Track Wefunder fundraise campaign in Enzo
- Manage cap table for Wefunder raise in Ume

---

## 15. Creator Subscription & Membership

---

### Patreon (`patreon`)

**Primary App:** `dongo`, `ayo`, `shango`
**Integration Type:** Creator membership and subscription platform connector
**Capability Required:** `network.outbound`, `financial.read`, `ipc.write:ayo.*`

**What It Is:** Patreon is a membership platform that allows creators to build subscription-based businesses, offering exclusive content and community access to paying patrons.

**How It Works in ogun OS:** Patreon is one of the most important integrations for creator enterprises in ogun OS. Patreon monthly subscription revenue is the foundational MRR metric for the creator enterprise — reconciled in Dongo and displayed prominently in the Enzo enterprise dashboard. Patron count and subscription tiers are tracked in Qala. Churn rate is monitored by the OBSERVATORY_AGENT.

Within `ayo`, the Patreon page is linked as the operator's primary membership community. Patron-only content can be produced in Shango's content pipeline and distributed through Patreon.

The Pricing Agent monitors Patreon tier pricing vs. benchmark patron LTV to recommend tier structure optimization.

**Functions on the Platform:**
- Reconcile Patreon subscription revenue as MRR in Dongo — a core creator enterprise KPI
- Display Patreon patron count, MRR, and tier breakdown in Enzo enterprise dashboard
- Monitor patron growth and churn in Qala Observatory
- Link Patreon page in Ayo digital spaces and Heshima Linktree
- Enable Pricing Agent to analyze Patreon tier pricing vs. patron LTV benchmarks
- Enable Productization Agent to identify Patreon content patterns suitable for scaling
- Feed Patreon MRR to passive income ratio calculations

---

### Kit (`kit`) (formerly ConvertKit)

**Primary App:** `ayo`, `dongo`, `shango`
**Integration Type:** Email marketing and creator commerce connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Kit (formerly ConvertKit) is an email marketing and creator commerce platform used by bloggers, podcasters, course creators, and online business owners for list building, email automation, and digital product sales.

**How It Works in ogun OS:** Kit integrates with `ayo` as the operator's primary email list and newsletter platform. Subscriber count and email engagement metrics (open rates, click rates) are pulled into Qala. Kit commerce revenue (digital product sales through Kit) is reconciled in Dongo. Email list growth is tracked as an audience growth KPI in Enzo.

**Functions on the Platform:**
- Pull Kit subscriber count and email engagement metrics into Qala Observatory
- Reconcile Kit digital product and course sales in Dongo
- Track email list growth as an audience growth KPI in Enzo enterprise dashboard
- Embed Kit newsletter subscribe form links in Ayo spaces and Heshima Linktree
- Feed email list data to the Acquisition Agent for audience expansion analysis

---

## 16. AI, Knowledge & Productivity Tools

---

### ChatGPT / OpenAI (`chatgpt`)

**Primary App:** `sambara` (Agent Driver), `ogun-assistant` (OBA)
**Integration Type:** LLM driver for Sambara agent system
**Capability Required:** `network.outbound`, `agent.execute`

**What It Is:** ChatGPT and the OpenAI API provide access to GPT-4o, o1, o1-mini, and o3-mini language models for AI reasoning, generation, and task completion.

**How It Works in ogun OS:** OpenAI/ChatGPT is one of the four built-in LLM drivers in Sambara (`openai-chatgpt`). Any Sambara agent can be configured to use OpenAI models as its primary or fallback intelligence backend. The OpenAI API key is stored securely in the Sambara vault — never exposed in configuration files, logs, or telemetry.

Within `ogun-assistant` (OBA), the operator can configure OBA to use a specific OpenAI model for their AI assistant conversations.

**Functions on the Platform:**
- Power any Sambara agent's reasoning via the `openai-chatgpt` driver (`gpt-4o`, `o1`, `o3-mini`)
- Serve as fallback LLM driver when primary model (Claude) is unavailable
- Power OBA (ogun AI Assistant) conversations when configured as the primary assistant model
- Enable `o1`/`o3-mini` usage for math-intensive and logic-heavy agent tasks (OPTIMIZER, ANALYST types)
- Feed token usage costs to Sambara's per-agent cost tracking

---

### Notion (`notion`)

**Primary App:** `akeel`, `moto`, `shango`
**Integration Type:** External knowledge base and workspace connector
**Capability Required:** `network.outbound`, `ipc.write:akeel.*`

**What It Is:** Notion is an all-in-one workspace for notes, wikis, project management, and databases — widely used by individuals and teams for knowledge management and project tracking.

**How It Works in ogun OS:** Notion integrates with `akeel` as an external knowledge base source. Notion pages and databases can be synced into Akeel's knowledge base, making Notion content searchable within the ogun OS semantic search system. Notion projects can be synced as Moto work packages. The operator transitioning to ogun OS from Notion can migrate knowledge assets into the native Akeel system.

**Functions on the Platform:**
- Sync Notion pages and databases into Akeel's knowledge base
- Import Notion project databases as Moto work packages
- Index Notion content in the ogun semantic filesystem
- Support knowledge migration from Notion to native Akeel
- Provide read access to Notion content for Sambara agents with appropriate capability

---

### Evernote (`evernote`)

**Primary App:** `akeel`, `ogun-notes`
**Integration Type:** Note and knowledge migration connector
**Capability Required:** `network.outbound`, `ipc.write:akeel.*`

**What It Is:** Evernote is a note-taking and organization application used for capturing and organizing notes, documents, and web clips.

**How It Works in ogun OS:** Evernote integrates with `akeel` and `ogun-notes` as a knowledge migration and sync source. Evernote notebooks and notes can be imported into Akeel or ogun-notes. The integration supports operators transitioning from Evernote to native ogun OS knowledge management.

**Functions on the Platform:**
- Sync Evernote notebooks into Akeel knowledge base
- Import Evernote notes into ogun-notes for quick-capture migration
- Enable Akeel semantic search over imported Evernote content

---

### Reflect (`reflect`)

**Primary App:** `akeel`
**Integration Type:** Networked note-taking connector
**Capability Required:** `network.outbound`, `ipc.write:akeel.*`

**What It Is:** Reflect is a networked note-taking app that mirrors your notes to a local graph, offering back-linked, AI-assisted knowledge management.

**How It Works in ogun OS:** Reflect integrates as an external knowledge graph that syncs note content into Akeel's knowledge base. Back-links and note relationships from Reflect enrich the Akeel knowledge graph.

**Functions on the Platform:**
- Sync Reflect notes and back-links into Akeel knowledge graph
- Enable ogun semantic search over Reflect note content

---

### Grammarly (`grammarly`)

**Primary App:** `shango`, `kogi`, `ayo`
**Integration Type:** Writing assistance and quality connector
**Capability Required:** `network.outbound`

**What It Is:** Grammarly is an AI-powered writing assistant that provides grammar checking, style suggestions, clarity improvements, and tone detection.

**How It Works in ogun OS:** Grammarly integrates as a writing quality layer accessible within the ogun OS text editor surfaces (notes, proposals, content drafts in Shango, email drafts in Kogi). Grammarly suggestions are displayed inline in the editor. Grammarly Business API enables integration directly within the Shango content production pipeline as a quality gate before content artifacts are finalized.

**Functions on the Platform:**
- Provide inline grammar and style suggestions in ogun OS text editors
- Serve as a quality gate in Shango's content production pipeline
- Improve proposal and client communication quality in Kogi
- Review draft content before publishing from Ayo's content interface

---

### Akiflow (`akiflow`)

**Primary App:** `kogi`, `misimu`
**Integration Type:** Task and calendar unification connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Akiflow is a task consolidation and daily planning tool that aggregates tasks from multiple platforms (Gmail, Asana, Jira, etc.) into a unified daily planning view.

**How It Works in ogun OS:** Akiflow integrates with `kogi`'s Filtering System to surface consolidated task views from connected external systems. Akiflow's time blocking recommendations sync to Misimu's calendar. This is particularly useful for operators using multiple external tools during a transition to native ogun OS task management.

**Functions on the Platform:**
- Surface Akiflow consolidated task views in Kogi's unified desk
- Sync Akiflow time blocks to Misimu calendar
- Route Akiflow task updates to ogun-tasks

---

### Todoist (`todoist`)

**Primary App:** `ogun-tasks`, `kogi`
**Integration Type:** Task management connector
**Capability Required:** `network.outbound`, `ipc.write:ogun-tasks.*`

**What It Is:** Todoist is a popular task management application used by individuals and teams for to-do lists and project task tracking.

**How It Works in ogun OS:** Todoist integrates as an external task source. Tasks and projects from Todoist sync into `ogun-tasks`, allowing the operator to manage their full task universe within ogun OS. Overdue Todoist tasks surface as priority items in Kogi's Filtering System.

**Functions on the Platform:**
- Sync Todoist tasks and projects into ogun-tasks
- Surface Todoist overdue items in Kogi's priority queue
- Reconcile Todoist task completion with Moto project tracking

---

### Trello (`trello`)

**Primary App:** `moto`, `kogi`
**Integration Type:** Project and task board connector
**Capability Required:** `network.outbound`, `ipc.write:moto.*`

**What It Is:** Trello is a visual project management tool using Kanban-style boards, cards, and lists.

**How It Works in ogun OS:** Trello boards sync as Moto project workspaces. Trello cards map to Moto work packages and tasks. Trello card updates trigger engagement status changes in Kogi when a card represents a client deliverable.

**Functions on the Platform:**
- Sync Trello boards as Moto project workspaces
- Map Trello cards to Moto work packages
- Trigger Kogi engagement updates on Trello card completion

---

### Airtable (`airtable`)

**Primary App:** `akeel`, `moto`, `dongo`
**Integration Type:** Database and spreadsheet connector
**Capability Required:** `network.outbound`, `ipc.write:akeel.*`

**What It Is:** Airtable is a flexible database tool used for CRM, project tracking, content calendars, inventory management, and more.

**How It Works in ogun OS:** Airtable bases integrate with multiple ogun OS apps depending on their configured purpose. CRM Airtable bases sync as Kogi client records. Content calendar Airtable bases inform Ayo's content publishing schedule. Inventory Airtable bases sync with Shango's inventory management. Financial tracking Airtable bases feed data to Dongo's reconciliation.

**Functions on the Platform:**
- Sync Airtable CRM bases to Kogi client management
- Feed Airtable content calendars to Ayo's publishing schedule
- Connect Airtable inventory databases to Shango inventory management
- Surface Airtable data within Akeel for search and knowledge access

---

### Lindy (`lindy`)

**Primary App:** `sambara`
**Integration Type:** AI automation and agent workflow connector
**Capability Required:** `network.outbound`, `agent.execute`

**What It Is:** Lindy is an AI automation platform for building personal AI assistants and automated workflows.

**How It Works in ogun OS:** Lindy integrates with `sambara` as an external automation provider. Operators can configure Lindy automations to be triggered by Sambara agent events, or use Lindy-built workflows to extend Sambara's EXECUTE_BOUNDED capabilities for specific use cases not yet covered by native Sambara agents.

**Functions on the Platform:**
- Trigger Lindy automation workflows from Sambara agent outputs
- Surface Lindy automation results in Kogi or ogun-messenger
- Extend Sambara agent capability coverage with Lindy-built workflows

---

### Taskade Genesis (`taskadegenesis`)

**Primary App:** `sambara`, `moto`
**Integration Type:** AI project management and agent workflow connector
**Capability Required:** `network.outbound`, `ipc.write:moto.*`

**What It Is:** Taskade Genesis is an AI-powered project management and team collaboration platform with native AI agent workflows.

**How It Works in ogun OS:** Taskade Genesis integrates with `sambara` for agent workflow interoperability and with `moto` for project synchronization. Taskade projects and AI task completions sync as Moto work package updates.

**Functions on the Platform:**
- Sync Taskade projects to Moto work packages
- Interoperate Taskade AI task completions with Sambara agent workflows
- Surface Taskade task updates in Kogi's unified desk

---

### Simplify (`simplify`)

**Primary App:** `kogi`, `dongo`
**Integration Type:** Job application and career management connector
**Capability Required:** `network.outbound`

**What It Is:** Simplify is a job application autofill and tracking tool used by job seekers and contractors managing multiple active applications.

**How It Works in ogun OS:** Simplify integrates with `kogi` as a job application pipeline management tool for operators in job-search or contract-hunting mode. Application statuses sync to Kogi's pipeline.

**Functions on the Platform:**
- Sync Simplify job application statuses to Kogi's pipeline
- Track application success rate as a pipeline metric

---

## 17. Development & Code Hosting

---

### GitHub (`github`)

**Primary App:** `mizeez`, `shango`, `moto`
**Integration Type:** Code hosting, CI/CD, and version control connector
**Capability Required:** `network.outbound`, `ipc.write:mizeez.*`, `ipc.write:shango.*`

**What It Is:** GitHub is the world's largest code hosting platform, used by developers for version control, open-source collaboration, CI/CD pipelines, and project management.

**How It Works in ogun OS:** GitHub is one of the three code hosting platforms that ogun OS itself is mirrored on (in addition to GitLab and Codeberg). As an integration, GitHub connects to `mizeez` as a code repository and artifact source. GitHub repositories sync to Mizeez's version control registry. GitHub Actions CI/CD pipeline results are tracked in Shango's QA and testing management. GitHub Issues and Projects sync to Moto work packages.

**Functions on the Platform:**
- Sync GitHub repositories and branches in Mizeez's version control registry
- Track GitHub Actions CI/CD pipeline results in Shango's QA management
- Sync GitHub Issues to Moto work packages
- Pull GitHub repository health metrics (commit frequency, open PRs, issue count) into Qala Observatory
- Surface GitHub release artifacts in Mizeez's artifact repository
- Register GitHub-hosted artifacts in the Shango distribution pipeline

---

### GitLab (`gitlab`)

**Primary App:** `mizeez`, `shango`, `moto`
**Integration Type:** Code hosting and DevOps platform connector
**Capability Required:** `network.outbound`, `ipc.write:mizeez.*`

**What It Is:** GitLab is an all-in-one DevOps platform for code hosting, CI/CD, project management, and security scanning — and the primary repository host for ogun OS itself.

**How It Works in ogun OS:** GitLab is the primary code hosting integration for ogun OS operators building software. GitLab repositories, CI/CD pipelines, merge requests, and issues integrate with `mizeez`, `shango`, and `moto` using the same architecture as the GitHub integration, with full GitLab pipeline support.

**Functions on the Platform:**
- Sync GitLab repositories and MR status in Mizeez
- Track GitLab CI/CD pipeline results in Shango's production pipeline
- Sync GitLab Issues and milestones to Moto work packages
- Pull GitLab pipeline success rates into Qala Observatory

---

### Codeberg (`codeberg`)

**Primary App:** `mizeez`
**Integration Type:** Open-source code hosting connector
**Capability Required:** `network.outbound`, `ipc.write:mizeez.*`

**What It Is:** Codeberg is a free, open-source code hosting platform based on Forgejo, serving as an alternative to GitHub and GitLab for privacy-conscious developers and open-source projects. ogun OS is also mirrored on Codeberg.

**How It Works in ogun OS:** Codeberg integrates with `mizeez` as an open-source repository mirror and code hosting source.

**Functions on the Platform:**
- Sync Codeberg repositories in Mizeez's version control registry
- Track Codeberg repository activity metrics

---

### Zapier (`zapier`)

**Primary App:** `sambara`, `kogi`, `ayo`
**Integration Type:** No-code automation and workflow connector
**Capability Required:** `network.outbound`

**What It Is:** Zapier is a no-code automation platform that connects thousands of apps through trigger-action workflows ("Zaps").

**How It Works in ogun OS:** Zapier integrates with `sambara` as an external automation orchestration layer. For apps not yet natively integrated with ogun OS, Zapier serves as a bridge — routing data between third-party tools and ogun OS APIs. Zapier Zaps can be triggered by ogun OS webhook events and can write data back to ogun OS via the public API.

**Functions on the Platform:**
- Connect third-party apps to ogun OS via Zapier webhooks and Zap triggers
- Route external automation outputs to ogun-messenger or Kogi pipeline
- Enable operators to build custom integration bridges for niche tools
- Serve as a fallback integration layer for tools without native connectors

---

### Zoho (`zoho`)

**Primary App:** `kogi`, `ume`, `dongo`
**Integration Type:** Business operations suite connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Zoho is a comprehensive business software suite covering CRM, accounting, HR, project management, and more — used by small businesses and independent operators globally.

**How It Works in ogun OS:** Zoho integrates as a multi-module connector. Zoho CRM contacts and deals sync to Kogi's client management and pipeline. Zoho Books transactions sync to Dongo's accounting. Zoho Projects tasks sync to Moto.

**Functions on the Platform:**
- Sync Zoho CRM deals and contacts to Kogi pipeline and client management
- Reconcile Zoho Books transactions in Dongo
- Sync Zoho Projects tasks to Moto work packages

---

## 18. Project Management & Collaboration

---

### Asana (`asana`)

**Primary App:** `moto`, `kogi`
**Integration Type:** Project management connector
**Capability Required:** `network.outbound`, `ipc.write:moto.*`

**What It Is:** Asana is a project and task management platform used by teams and solopreneurs for tracking work, deadlines, and project progress.

**How It Works in ogun OS:** Asana projects and tasks sync to `moto`'s work package registry. Asana task completions trigger Kogi engagement status updates. Asana milestone completions feed Qala Observatory as project health signals.

**Functions on the Platform:**
- Sync Asana projects and tasks to Moto work package registry
- Trigger Kogi engagement updates on Asana task completion
- Pull Asana project health metrics into Qala Observatory

---

### Jira (`jira`)

**Primary App:** `moto`, `shango`, `mizeez`
**Integration Type:** Software project and issue tracking connector
**Capability Required:** `network.outbound`, `ipc.write:moto.*`

**What It Is:** Jira is a project and issue tracking platform primarily used by software development teams for sprint planning, bug tracking, and agile project management.

**How It Works in ogun OS:** Jira issues sync to Moto as work packages. Jira epics map to Moto projects. Shango's QA management integrates with Jira bug tracking. Sprint velocity and completion data feed Qala Observatory.

**Functions on the Platform:**
- Sync Jira issues to Moto work packages
- Map Jira epics to Moto projects
- Connect Jira bug tracking to Shango QA management
- Pull sprint velocity and burndown metrics into Qala Observatory

---

### Monday.com (`monday.com`)

**Primary App:** `moto`, `kogi`
**Integration Type:** Work management connector
**Capability Required:** `network.outbound`, `ipc.write:moto.*`

**What It Is:** Monday.com is a visual work management platform used for project tracking, CRM, and business operations by teams and independent operators.

**How It Works in ogun OS:** Monday.com boards and items sync to Moto and Kogi with appropriate mapping. CRM boards sync to Kogi pipeline. Project boards sync to Moto work packages.

**Functions on the Platform:**
- Sync Monday.com CRM boards to Kogi pipeline management
- Sync Monday.com project boards to Moto work packages
- Pull Monday.com board metrics into Qala Observatory

---

### SignNow (`signnow`)

**Primary App:** `ume`
**Integration Type:** Electronic signature connector
**Capability Required:** `network.outbound`, `ipc.write:ume.*`

**What It Is:** SignNow is an electronic signature and document signing platform used by businesses for contract execution.

**How It Works in ogun OS:** SignNow integrates with `ume`'s contract lifecycle management as an e-signature connector. Contracts created in Ume's contract template library are sent to SignNow for execution. Signed documents are returned and stored in Ume's contract records. Execution status updates are tracked in Ume's obligation management.

**Functions on the Platform:**
- Send Ume contracts to SignNow for electronic signature execution
- Return signed documents to Ume's contract records
- Track signature status as a contract lifecycle milestone in Ume
- Trigger Kogi engagement activation on contract execution (Ọpọn rule `opn-003`)

---

## 19. Banking, Payments & Money Transfer (Additional)

---

### QuickBooks (`quickbooks`)

**Primary App:** `dongo`, `ume`
**Integration Type:** Small business accounting connector
**Capability Required:** `network.outbound`, `financial.read`, `financial.write`

**What It Is:** QuickBooks is the most widely used small business accounting software for invoicing, expense tracking, payroll, and tax management.

**How It Works in ogun OS:** QuickBooks integrates with `dongo` as a bidirectional accounting sync. ogun OS can serve as the primary operational system while QuickBooks serves as the external accounting system for tax filing and accountant access. Transactions recorded in Dongo can be synced to QuickBooks, and QuickBooks data is importable into Dongo for operators transitioning to native ogun OS accounting.

**Functions on the Platform:**
- Bidirectional transaction sync between Dongo and QuickBooks
- Push Dongo financial data to QuickBooks for accountant access and tax filing
- Pull QuickBooks historical data into Dongo for operators migrating from QuickBooks
- Support the Bookkeeping Agent in reconciling transactions across both systems

---

### Good Budget (`goodbudgets`)

**Primary App:** `dongo`, `zamani`
**Integration Type:** Envelope budgeting connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Goodbudget is an envelope-based budgeting app that helps individuals and families manage spending using digital envelope categories.

**How It Works in ogun OS:** Goodbudget integrates with `zamani`'s personal finance management as a household budget source. Goodbudget envelope balances and transaction history sync into Zamani's personal finance and accounting module.

**Functions on the Platform:**
- Sync Goodbudget envelope balances to Zamani personal finance
- Pull Goodbudget spending history into Zamani personal budget management

---

### EveryDollar (`everydollar`)

**Primary App:** `zamani`
**Integration Type:** Zero-based budgeting connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** EveryDollar is a zero-based budgeting app by Ramsey Solutions.

**How It Works in ogun OS:** EveryDollar integrates with Zamani's personal finance module for household budget tracking alongside business finance in Dongo.

**Functions on the Platform:**
- Sync EveryDollar budget data to Zamani personal finance module

---

### Empower (`empower`)

**Primary App:** `zamani`, `igi`
**Integration Type:** Personal finance and wealth management connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Empower (formerly Personal Capital) is a personal finance and investment management platform with portfolio tracking, budgeting, and retirement planning.

**How It Works in ogun OS:** Empower connects to `zamani` for net worth and personal portfolio tracking. Investment holdings from Empower are synced to `igi`'s portfolio management as personal investment assets. Retirement account projections from Empower feed Zamani's estate and retirement planning.

**Functions on the Platform:**
- Sync Empower net worth and portfolio data to Zamani
- Import Empower investment holdings to Igi portfolio management
- Feed Empower retirement projections to Zamani estate planning

---

### YNAB (`ynab`)

**Primary App:** `zamani`
**Integration Type:** Zero-based budgeting connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** YNAB (You Need A Budget) is a zero-based budgeting app for personal and household finance management.

**How It Works in ogun OS:** YNAB integrates with Zamani's personal finance module. YNAB budget categories and transactions sync into Zamani for a unified view of personal and business finances.

**Functions on the Platform:**
- Sync YNAB budget data and transactions to Zamani personal finance
- Track YNAB budget adherence as a personal financial health metric

---

### WalletHub (`wallethub`)

**Primary App:** `zamani`
**Integration Type:** Credit monitoring connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** WalletHub is a personal finance site offering free credit score monitoring, credit cards, and financial product comparisons.

**How It Works in ogun OS:** WalletHub connects to Zamani for credit score monitoring. Credit score history is tracked as part of the personal financial health dashboard.

**Functions on the Platform:**
- Pull WalletHub credit score data into Zamani personal finance
- Track credit score trend as a personal financial health metric

---

### Monarch (`monarch`)

**Primary App:** `zamani`, `dongo`
**Integration Type:** Personal finance connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Monarch Money is a modern personal finance app offering budgeting, investment tracking, and net worth visualization.

**How It Works in ogun OS:** Monarch integrates with Zamani for personal finance management. Monarch investment holdings and net worth data sync to Zamani's wealth management dashboard.

**Functions on the Platform:**
- Sync Monarch net worth and account data to Zamani
- Import Monarch investment holdings to Igi portfolio management

---

## 20. Design & Creative Tools

---

### Canva (`canva`)

**Primary App:** `shango`, `ayo`, `akeel`
**Integration Type:** Graphic design and content creation connector
**Capability Required:** `network.outbound`, `ipc.write:shango.*`

**What It Is:** Canva is a cloud-based graphic design platform used by creators, marketers, and small businesses for social media graphics, presentations, documents, and visual content.

**How It Works in ogun OS:** Canva integrates with `shango` as a visual content production tool within the content factory. Canva designs are exported as artifacts and stored in the VFS. The Shango production pipeline can trigger Canva template creation as part of a content production workflow.

**Functions on the Platform:**
- Export Canva designs as registered artifacts in the VFS
- Trigger Canva template production from Shango's content pipeline
- Index design assets in Akeel's asset library
- Track design production volume in Qala

---

### Figma (`figma`)

**Primary App:** `shango`, `mizeez`, `akeel`
**Integration Type:** UI/UX design and prototyping connector
**Capability Required:** `network.outbound`, `ipc.write:shango.*`

**What It Is:** Figma is a cloud-based UI/UX design and prototyping tool used by designers and product teams for interface design, wireframing, and design system management.

**How It Works in ogun OS:** Figma integrates with `shango` as a design production environment and with `mizeez` for design artifact version control. Figma file versions sync to Mizeez's artifact repository. Design files are exported and registered as deliverable artifacts in the VFS.

**Functions on the Platform:**
- Sync Figma file versions to Mizeez's artifact version control
- Export Figma designs as registered deliverable artifacts
- Track design iteration count and review cycles in Shango's QA management
- Link Figma prototypes to Moto project deliverables

---

### MuseScore (`musescore`)

**Primary App:** `shango`, `akeel`, `didara`
**Integration Type:** Music notation and sheet music connector
**Capability Required:** `network.outbound`, `ipc.write:shango.*`

**What It Is:** MuseScore is an open-source music notation software used by musicians and composers for writing and publishing sheet music.

**How It Works in ogun OS:** MuseScore integrates with `shango` as a music production environment. Completed scores are exported as artifacts and registered in the VFS. Sheet music publications are tracked in `didara` as IP assets with copyright registration metadata.

**Functions on the Platform:**
- Export MuseScore notation files as registered artifacts
- Track published sheet music as IP assets in Didara
- Index musical works in Akeel's knowledge base

---

### Dorico (`dorico`)

**Primary App:** `shango`, `didara`
**Integration Type:** Professional music notation connector
**Capability Required:** `network.outbound`

**What It Is:** Dorico is Steinberg's professional music notation and scoring software used by professional composers and arrangers.

**How It Works in ogun OS:** Same architecture as MuseScore. Dorico scores export as artifacts and track in Didara as IP.

**Functions on the Platform:**
- Export Dorico scores as registered artifacts
- Track compositions as IP assets in Didara

---

## 21. Calendar, Scheduling & CRM

---

### Calendly (`calendly`)

**Primary App:** `misimu`, `kogi`, `heshima`
**Integration Type:** Appointment scheduling connector
**Capability Required:** `network.outbound`, `ipc.write:misimu.*`

**What It Is:** Calendly is a scheduling automation platform used by consultants, coaches, and service providers for booking appointments and client calls.

**How It Works in ogun OS:** Calendly integrates with `misimu` as the operator's external booking page. Calendly appointments sync to the Misimu calendar. New bookings trigger Kogi pipeline entries as incoming client engagements. Calendly booking volume is tracked in Qala as an acquisition metric.

**Functions on the Platform:**
- Sync Calendly appointments to Misimu calendar
- Convert new Calendly bookings to Kogi pipeline entries
- Track booking volume as a pipeline acquisition metric in Qala Observatory
- Embed Calendly booking link in Heshima Linktree and Ayo digital spaces
- Enable the Acquisition Agent to monitor booking conversion rates

---

### Clay (`clay`)

**Primary App:** `kogi`, `heshima`
**Integration Type:** CRM and network intelligence connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Clay is a powerful CRM and data enrichment tool that aggregates contact data from dozens of sources for prospecting, research, and relationship management.

**How It Works in ogun OS:** Clay integrates with `kogi` as a contact enrichment and pipeline research tool. Clay enriched prospect data can be imported into Kogi's pipeline as lead entries. Clay's relationship intelligence informs the Acquisition Agent's outreach targeting at RECOMMEND authority.

**Functions on the Platform:**
- Import Clay enriched prospect data to Kogi pipeline as leads
- Enrich ogun-contacts with Clay's data aggregation
- Inform Acquisition Agent outreach targeting with Clay prospect signals

---

### Capsule (`capsule`)

**Primary App:** `kogi`, `ogun-contacts`
**Integration Type:** CRM connector
**Capability Required:** `network.outbound`, `ipc.write:kogi.*`

**What It Is:** Capsule CRM is a lightweight CRM tool used by small businesses and freelancers for tracking client relationships and sales pipelines.

**How It Works in ogun OS:** Capsule CRM contacts and opportunities sync to Kogi's client management and pipeline. Capsule's opportunity pipeline value contributes to EPV calculations in Enzo.

**Functions on the Platform:**
- Sync Capsule CRM contacts to ogun-contacts and Kogi client management
- Map Capsule opportunities to Kogi pipeline entries
- Include Capsule pipeline value in EPV calculations

---

## 22. Writing & Document Tools

---

### Google Workspace (`googleworkspace`)

**Primary App:** `misimu`, `akeel`, `shango`, `ogun-messenger`
**Integration Type:** Productivity suite and document connector
**Capability Required:** `network.outbound`, `ipc.write:misimu.*`, `ipc.write:akeel.*`

**What It Is:** Google Workspace is Google's suite of productivity applications including Gmail, Google Calendar, Google Drive, Google Docs, Google Sheets, and Google Meet.

**How It Works in ogun OS:** Google Workspace is the broadest productivity suite integration in ogun OS. Google Calendar syncs to Misimu as a primary calendar source. Google Drive documents are indexable in Akeel's knowledge base. Gmail messages are routable to ogun-messenger. Google Meet appointments appear in Misimu calendar. Google Docs created in Shango's content pipeline can be saved to Google Drive as artifacts.

**Functions on the Platform:**
- Sync Google Calendar to Misimu as a primary calendar source
- Index Google Drive documents in Akeel's knowledge base
- Route Gmail to ogun-messenger's unified inbox
- Surface Google Meet calls in Misimu calendar
- Export Shango content artifacts to Google Drive
- Pull Google Workspace usage metrics to Qala

---

### Microsoft Workspace / Microsoft 365 (`microsoftworkspace`)

**Primary App:** `misimu`, `akeel`, `shango`, `ogun-messenger`
**Integration Type:** Microsoft productivity suite connector
**Capability Required:** `network.outbound`, `ipc.write:misimu.*`

**What It Is:** Microsoft 365 is Microsoft's productivity suite including Outlook, Teams, Word, Excel, PowerPoint, OneDrive, and SharePoint.

**How It Works in ogun OS:** Same architecture as Google Workspace with equivalent Microsoft platform mappings. Outlook Calendar syncs to Misimu. Outlook Mail routes to ogun-messenger. OneDrive documents index in Akeel. Teams meetings sync to Misimu calendar.

**Functions on the Platform:**
- Sync Outlook Calendar to Misimu
- Route Outlook Mail to ogun-messenger
- Index OneDrive documents in Akeel
- Surface Teams meetings in Misimu calendar

---

### Apple Workspace / iCloud (`appleworkspace`)

**Primary App:** `misimu`, `ogun-messenger`, `zamani`
**Integration Type:** Apple ecosystem connector
**Capability Required:** `network.outbound`, `ipc.write:misimu.*`

**What It Is:** Apple iCloud provides calendar, mail, notes, reminders, and document storage services tightly integrated with Apple devices.

**How It Works in ogun OS:** Apple iCloud Calendar syncs to Misimu on macOS installations. iCloud Mail routes to ogun-messenger. iCloud Notes content can be imported into ogun-notes or Akeel.

**Functions on the Platform:**
- Sync iCloud Calendar to Misimu (macOS/iOS targets)
- Route iCloud Mail to ogun-messenger
- Import iCloud Notes to ogun-notes

---

## 23. Accounting & Finance Tools

---

### Pomofocus / Pomodoro (`pomofocus`, `pomodoro`)

**Primary App:** `ogun-focus`, `kogi`
**Integration Type:** Focus session and time-tracking connector
**Capability Required:** `network.outbound`

**What It Is:** Pomofocus and Pomodoro-based timers are focus management tools using the Pomodoro Technique (25-minute focused work sessions with short breaks).

**How It Works in ogun OS:** Pomofocus and Pomodoro timers integrate with `ogun-focus` as external session sources. Completed focus sessions can be imported into ogun-focus's session log and attributed to the active enterprise and engagement. Session data feeds Kogi's productivity analytics.

**Functions on the Platform:**
- Import completed Pomodoro sessions into ogun-focus session log
- Attribute focus session time to active engagements in Kogi
- Feed focus session data to Kogi's productivity analytics

---

### Subpage (`subpage`)

**Primary App:** `ayo`, `heshima`, `shango`
**Integration Type:** Content page and landing page connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Subpage is a link-in-bio and content page builder used by creators to organize and share their content and links in a single customizable page.

**How It Works in ogun OS:** Subpage integrates with `ayo` as an external link page/digital space. The Subpage URL is embedded in Heshima's Linktree and Ayo profile pages. Subpage click analytics are pulled into Qala.

**Functions on the Platform:**
- Register Subpage as an external digital space in Ayo
- Embed Subpage link in Heshima Linktree
- Pull Subpage click analytics into Qala Observatory

---

### Bazel44 (`bazel44`)

**Primary App:** `shango`, `mizeez`
**Integration Type:** Build system connector
**Capability Required:** `network.outbound`, `ipc.write:shango.*`

**What It Is:** Bazel is a build system used by software engineering teams for fast, reproducible builds. "Bazel44" references Bazel-based build tooling.

**How It Works in ogun OS:** Bazel build systems integrate with `shango`'s production pipeline and `mizeez`'s artifact management. Build results from Bazel pipelines are tracked in Shango's QA management. Build artifacts register in Mizeez's artifact repository.

**Functions on the Platform:**
- Track Bazel build results in Shango's QA and production pipeline
- Register Bazel build artifacts in Mizeez's artifact repository
- Pull build performance metrics into Qala Observatory

---

## 24. Website & Portfolio Builders (Additional)

---

### Linktree (`linktree`) / Link (`link`)

**Primary App:** `heshima`, `ayo`
**Integration Type:** External link profile connector
**Capability Required:** `network.outbound`, `ipc.write:heshima.*`

**What It Is:** Linktree is the original link-in-bio tool that organizes multiple links behind a single shareable URL — used by creators and professionals to point followers to their various platforms and content.

**How It Works in ogun OS:** Linktree integrates with `heshima`'s Linktree/Linkforest/Linknet management as an external link profile source. The operator's existing Linktree can be imported into Heshima's native link management system, enabling ogun OS to serve as the source of truth for all link profiles. Linktree click analytics are pulled into Qala.

**Functions on the Platform:**
- Import existing Linktree links into Heshima's native link management
- Pull Linktree click analytics into Qala Observatory
- Gradually migrate link traffic from Linktree to native Ayo space with Heshima link management

---

## 25. Music & Audio Platforms

---

### Spotify (`spotify`)

**Primary App:** `ayo`, `dongo`, `shango`
**Integration Type:** Music and podcast distribution connector
**Capability Required:** `network.outbound`, `ipc.write:ayo.*`

**What It Is:** Spotify is the world's largest music and podcast streaming platform, with distribution and monetization for musicians and podcasters through royalties and Spotify for Podcasters.

**How It Works in ogun OS:** Spotify integrates with `ayo` and `shango` as a music and podcast distribution channel. Published content on Spotify is tracked in the Ayo space as a content channel. Spotify streaming royalties and podcast advertising revenue are reconciled in Dongo as attributed income streams. Spotify for Artists analytics (monthly listeners, streams, follower count) pull into Qala.

**Functions on the Platform:**
- Track Spotify monthly listeners, streams, and follower count in Qala Observatory
- Reconcile Spotify royalty payments as attributed income in Dongo
- Include Spotify music in the music IP registry in Didara
- Track podcast episode download count as a content production metric
- Display Spotify profile in Heshima Linktree and Ayo spaces

---

### Pandora (`pandora`)

**Primary App:** `ayo`, `dongo`
**Integration Type:** Music distribution and royalty connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** Pandora is a music streaming platform with artist tools for music distribution and digital streaming royalty collection.

**How It Works in ogun OS:** Pandora royalty payments reconcile in Dongo as music income. Streaming metrics pull into Qala for music creator enterprise tracking.

**Functions on the Platform:**
- Reconcile Pandora royalties in Dongo
- Track Pandora streaming metrics in Qala Observatory

---

### Apple Podcasts (`applepodcasts`)

**Primary App:** `ayo`, `shango`
**Integration Type:** Podcast distribution connector
**Capability Required:** `network.outbound`

**What It Is:** Apple Podcasts is the largest podcast directory, used by podcast creators for distribution and discovery.

**How It Works in ogun OS:** Apple Podcasts integrates with `shango` as a podcast distribution channel. Episode production in Shango's content pipeline publishes to Apple Podcasts. Download metrics pull into Qala.

**Functions on the Platform:**
- Publish podcast episodes via Shango's content pipeline to Apple Podcasts
- Pull Apple Podcasts download and subscriber metrics into Qala

---

### Pocket Casts (`pocketcasts`)

**Primary App:** `ayo`
**Integration Type:** Podcast distribution connector
**Capability Required:** `network.outbound`

**What It Is:** Pocket Casts is a podcast player and discovery app used for podcast distribution and listener metrics.

**How It Works in ogun OS:** Pocket Casts RSS metrics integrate with Qala for podcast audience tracking.

**Functions on the Platform:**
- Track podcast listener metrics from Pocket Casts in Qala Observatory

---

### Overcast (`overcast`)

**Primary App:** `ayo`
**Integration Type:** Podcast distribution connector
**Capability Required:** `network.outbound`

**What It Is:** Overcast is a podcast player with a dedicated listener base for independent podcasters.

**How It Works in ogun OS:** Overcast statistics integrate with podcast distribution tracking in Qala.

**Functions on the Platform:**
- Include Overcast listener data in Qala podcast metrics

---

### Art19 (`art19`)

**Primary App:** `shango`, `dongo`, `ayo`
**Integration Type:** Professional podcast hosting and monetization connector
**Capability Required:** `network.outbound`, `financial.read`

**What It Is:** ART19 is a professional podcast hosting and monetization platform used by major media companies and independent podcasters for hosting, dynamic ad insertion, and audience analytics.

**How It Works in ogun OS:** ART19 integrates with `shango` as a professional podcast hosting and distribution platform. ART19 ad revenue and download metrics pull into Qala. Ad earnings reconcile in Dongo.

**Functions on the Platform:**
- Pull ART19 podcast download and ad performance metrics into Qala Observatory
- Reconcile ART19 ad insertion revenue in Dongo
- Track podcast audience growth in Enzo creator enterprise dashboard

---

## 26. Delivery, Food & Logistics

(See Section 11 — On-Demand & Service Marketplaces for Uber, Instacart, Grubhub, and DoorDash.)

---

## 27. Video & Streaming Platforms

(See Section 6 — Social Media & Content Distribution for YouTube and Twitch.)

---

## 28. Cloud Infrastructure

---

### Amazon Web Services (`amazonaws`)

**Primary App:** `apapo`, `shango`, `mizeez`
**Integration Type:** Cloud infrastructure and compute connector
**Capability Required:** `network.outbound`, `ipc.write:apapo.*`

**What It Is:** Amazon Web Services (AWS) is the world's largest cloud computing platform, offering compute, storage, databases, AI/ML, and hundreds of cloud services.

**How It Works in ogun OS:** AWS integrates with `apapo` (Hypergrid Platform) as a cloud infrastructure backend. Operators running software products, web services, or data pipelines on AWS can connect their AWS account to Apapo for infrastructure visibility, cost tracking, and resource management. AWS costs are reconciled in Dongo as business expenses. AWS resource health metrics surface in Qala Observatory. Shango's CI/CD pipelines can deploy to AWS environments managed in Apapo.

**Functions on the Platform:**
- Connect AWS account to Apapo for cloud infrastructure visibility and management
- Pull AWS resource health and utilization metrics into Qala Observatory
- Reconcile AWS bills as attributed business expenses in Dongo
- Track AWS spend as an infrastructure cost in Enzo enterprise dashboard
- Connect Shango's CI/CD pipelines to AWS deployment environments via Apapo
- Enable Sambara agents to monitor AWS CloudWatch alerts at OBSERVE authority
- Store AWS environment configuration in Apapo's environment registry

---

## Integration Framework Reference

### Capability Requirements by Integration Type

| Integration Type | Minimum Capabilities Required |
|---|---|
| Social media publishing | `network.outbound`, `ipc.write:ayo.*` |
| Financial income (read) | `financial.read`, `network.outbound` |
| Financial income (write) | `financial.read`, `financial.write`, `network.outbound` |
| Project/task management | `network.outbound`, `ipc.write:moto.*` |
| LLM driver | `network.outbound`, `agent.execute` |
| Code repository | `network.outbound`, `ipc.write:mizeez.*` |
| Calendar/scheduling | `network.outbound`, `ipc.write:misimu.*` |
| Knowledge/document | `network.outbound`, `ipc.write:akeel.*` |
| Field service | `network.outbound`, `ipc.write:kogi.*`, `financial.read` |
| Investment/portfolio | `network.outbound`, `financial.read` |

### Ọpọn Protocol Enforcement for Integrations

All third-party integration data is subject to the Ọpọn Protocol (`SYS-001`). Data received from an integration and attributed to Enterprise A is stored under `enterprise://[enterprise-A-id]/integrations/[service]/` and cannot be accessed by any process operating in the context of Enterprise B without explicit, logged, operator-approved cross-enterprise consent.

This means an operator running two separate Stripe accounts for two different enterprises will have completely isolated Stripe integration data — separate income streams, separate reconciliation histories, separate agent monitoring — even though both connect to Stripe through the same integration connector.

### Integration VFS Namespace Paths

| Integration Data Type | VFS Path Pattern |
|---|---|
| Integration raw data | `enterprise://[id]/integrations/[service]/raw/` |
| Synced income records | `enterprise://[id]/finance/income/[service]/` |
| Synced contacts | `enterprise://[id]/contacts/[service]/` |
| Analytics metrics | `telemetry://[enterprise-id]/integrations/[service]/` |
| Synced artifacts | `artifact://[enterprise-id]/[service]/[artifact-id]` |
| Integration credentials | `vault://sambara/keys/[service]-api-key` |

### Sambara Agent Integration Authority Matrix

| Agent | Integration Action | Authority Required |
|---|---|---|
| OBSERVATORY_AGENT | Monitor integration metrics | OBSERVE |
| FOLLOWUP_AGENT | Draft reply to integration inbox messages | RECOMMEND |
| PRICING_AGENT | Recommend integration pricing adjustments | RECOMMEND → EXECUTE_BOUNDED |
| BOOKKEEPING_AGENT | Reconcile integration transactions | EXECUTE_BOUNDED |
| ACQUISITION_AGENT | Monitor integration for prospect signals | OBSERVE → RECOMMEND |
| PRODUCTIZATION_AGENT | Detect integration pattern for productization | OBSERVE → EXECUTE_BOUNDED |

---

## TODO

add more integrations:

- claude
- chatgpt
- deepseek
- gemini
- grok
- replit
- lovable

- yahoo
- gmail

- vscode ogun os developer extension


- misc...
- linktree+ogun os integrations API/SDK

---

*ogun OS — Third-Party Integrations Specification*
*Version 0.1.0-alpha · Project Ogún · 2026*
*Owner: Dominic Eaton (@eatondo)*
