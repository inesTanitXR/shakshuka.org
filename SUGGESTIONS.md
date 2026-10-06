# shakshuka.org rebuild — notes and suggestions for Ines

**Goal: leave Wix completely (boycott).** Every Wix piece has a replacement in the table below.
Leila's review page (seven decisions, copy-ready reply): https://claude.ai/artifact/9qThCiexsEtnif1FFSrgDh — share it from the page's Share menu first. Source kept in `ref-review-page.html`.

| On Wix today | New home |
|---|---|
| Hosting | GitHub Pages, free |
| Events, RSVPs, donations, membership plans | Zeffy (Givebutter second) |
| Cookbook store | Zeffy shop, or PayPal/Square link, or email orders |
| Blog | pages on the new site |
| Forms | FormSubmit to their inbox |
| Newsletter | Buttondown / Mailchimp free tier |
| Members area, forum | dropped; WhatsApp/Signal group |
| Swag shop | dropped or Printful link |
| Domain | if registered through Wix, transfer out before closing the account |


Built 2026-10-06 (restyled same day on tanitxr.org/inessaid.com lines, no tile motifs). Preview: run `python3 build.py`, then open `docs/index.html` (or the local server).

## What I found on the current site

- **Platform:** Wix (Studio), with Wix Events for ticketing, Wix Stores for the cookbook,
  Wix Pricing Plans for membership, a Wix members area and a Wix blog.
- **Ticketing today:** Wix Events checkout. Wix adds a service fee on paid tickets
  (visible on their pages: $0.45 on an $18 ticket, $1.13 on $45, about 2.5%) on top of
  the card processing fee. Free events are also run through Wix Events with "sold out"
  caps.
- **Donations:** a Wix donation form ($50/$100/$200/$1,000, one time / monthly / yearly).
- **Membership:** two Wix plans, Tier Spéciale $50/yr and Tier Fabuleux $100/yr.
- **Legal:** 501(c)(3) public charity, EIN 92-3134851, founded 2023, Washington DC.
- **Images:** the home page is almost entirely AI-generated (Midjourney-style tiles,
  laughing groups, man with camel, man with lightbulb, fireworks over a medina, the
  "ornate wooden doors" header, the harissa illustration on the blog). All of them are
  gone. Kept: the logo, the seven board headshots, the Hallets' photo, the cookbook
  cover, the event posters/film stills/chef photos (these are the events' own artwork)
  and the Kairouan couscous-festival photo from the blog.
- **Tiles:** real photographed tiles only (Dar Lasram strip and dots, Qallaline panel from the Bardo, Barber mosque wall, Dar Cherait), all CC and credited; no drawn patterns.
- **Replacement photos:** 13 Creative Commons photos of Tunisia from Wikimedia Commons
  (Sidi Bou Said doors, Tunis medina, Kairouan, El Jem, Carthage, Cap Bon olives, Djerba
  weaving, brik, couscous, harissa, ojja, a Tunisian table). Every one is credited on
  `/credits/` and in `src-images/commons/CREDITS.md`. CC BY-SA photos require keeping the
  credit, which the page does.
- **Social media:** I could not find any Instagram, Facebook or LinkedIn page for
  Shakshuka.org. The site links to none. Ask them for handles; `SOCIALS` in `build.py`
  takes them and they appear in the footer. If they have an Instagram, their photos from
  the Iftar, the sing-along and the calligraphy workshop would replace a few of the
  Commons photos (the team page hero and the Iftar event, in particular).

## Things to confirm with them ([CHECK])

1. **Contact email.** The live site only shows the web designer's gmail. I used
   `info@shakshuka.org` everywhere (`CONTACT_EMAIL` in `build.py`). They need a real
   mailbox on the domain, and FormSubmit must be activated once from that mailbox
   (first form submission sends an activation link).
2. **Board bios.** I wrote short bios from the one-line descriptions on their team page.
   They should read and correct them.
3. **Dates on 2026 events** were given without a year on the site; I assumed 2026.
   The two "draft example" events (Cooking Class 5, Winter Sing-Along) are invented
   to show the reservation flows. They are not linked from the calendar; delete them or
   turn `draft=True` off once real dates exist.
4. **Stats on the home page:** "18+ events since 2024" is counted from their list;
   "~5,000 Tunisians in the DMV" is their own number from the contact page.
5. **Cookbook price $36** is from their store page; the "Purchase now" button still goes
   to the Wix store until a new checkout exists.
6. **Blog posts** link to the current Wix posts. Moving the five posts into this site is
   a half-hour job once they confirm the move.
7. **Event body texts** were written from their event pages, trimmed. Worth a read.

## Reservations and payments: what I recommend

The site is static (GitHub Pages), so checkout happens on a payment page the event
links to. The event page already has a "Reserve your seat" button that takes a
`reserve_url`, and free events get an inline RSVP form.

**Recommended: Zeffy.** Built for 501(c)(3)s, 100% free (no platform fee, no
processing fee; donors are asked for an optional tip at checkout). It does event tickets
with ticket tiers, capacity and QR check-in, recurring donations, membership plans,
embeddable forms and a donor database, and it sends tax receipts automatically.
It replaces three Wix apps at once (Events, Donations, Pricing Plans). Setup: create the
org account with the EIN, create one ticketing form per event, paste its link into
`reserve_url`. Donations and membership pages can embed Zeffy forms directly in this
site (iframe), which I will wire in as soon as they have an account.

Alternatives, in order:
- **Givebutter**: similar free model with tips, slightly nicer event pages, also has
  memberships. Good second choice.
- **Eventbrite**: the audience knows it and it brings discovery, but fees are about
  3.7% + $1.79 per paid ticket (free events are free). Fine for one-off big events like
  the Iftar if they want reach.
- **Humanitix**: fees go to charity, good ticketing, but less known in the US.
- **Stripe Payment Links** on their own: cheapest per transaction (2.9% + 30¢), no
  capacity/check-in tooling, and needs someone comfortable with Stripe.
- **Keep Wix Events**: possible, but then the site stays on Wix (hosting fee plus the
  per-ticket fee), and the design is limited to the Wix editor.

Free events: the RSVP form posts to their email through FormSubmit, no account needed.
If they want a headcount cap and automatic confirmations, a Zeffy free-ticket form does
that too.

Member discounts (free class seats, 25% off films): Zeffy and Givebutter both support
discount codes per ticket form; put the code in the membership welcome email.

## Other suggestions

- **Hosting:** GitHub Pages, like tanitxr.org and inessaid.com. Create a `shakshuka-org`
  repo, push, enable Pages from `main:/docs`, add a CNAME file and point the Wix DNS to
  GitHub. Zero hosting cost; they can cancel the Wix premium plan after the move.
- **Newsletter:** the forms collect emails to the mailbox. For a proper list, Buttondown
  (free up to 100 subscribers) or Mailchimp free tier; both give an embed form.
- **Photos:** ask them to send 20 to 30 of their own event photos. Real photos of real
  members beat any stock image and would replace most of the Commons photos.
- **Tunisia page:** currently Tanit XR, TAYP, the Tunisian Community Center, the
  Embassy, the cookbook, Our Tunisian Table, Zwïta, Khalil Ayed, Chef Salma Sellami, the
  films they screened, and three open spots with a suggestion form. They can send more.
- **Holidays page** on the old site is "under construction"; I left it out. A calendar of
  Tunisian holidays (Eid, Independence Day March 20, Women's Day August 13, Evacuation
  Day October 15) would be an easy addition.
- **Languages:** one language (English) for now, unlike our sites. French and Arabic
  can be added with the same translate.py approach if they want it.
- **Shak Swag shop:** a Wix print-on-demand store. I left it out of the new site; if they
  want it, link to a Printful/Printify storefront rather than hosting it here.
