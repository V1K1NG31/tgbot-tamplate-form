start-message =
    Hi 👋

    This is a <b>demo template bot</b>: a fictional studio called <b>Svetlitsa</b>
    helps you shape an idea — from a small landing page to a light brand kit.
    Everything below is <b>sample copy</b> you can swap for your product.

    The buttons open short “how it works in this example” sections.
    You can also fill out the form — submissions go to the bot’s admin chat.

    Pick a section 👇

menu-what =
    <b>Svetlitsa in this template</b> is a placeholder service: it shows how
    a menu with explanations and a “next step” button can look.
    In a real project, put your value proposition here.

menu-duration =
    For the demo we use about <b>2–6 weeks</b> for a typical mini-project.
    Real timelines are agreed with the client — in the template it is just
    text in <code>en.ftl</code>.

menu-price =
    The example uses <b>placeholder ranges</b> — no contract or payment.
    In production, replace this block with your pricing and packages.

    <i>This demo does not offer a free consultation — that line is only
    sample wording.</i>

menu-travel =
    <b>How we meet (example)</b>

    Work can be fully remote: calls, chat, a shared doc.
    If you need in-person sessions, say so in your own copy.

menu-property =
    <b>What the client usually gets (in the demo)</b>

    • Page or layout structure
    • Draft palette and typography
    • A short guide on using the assets

    <i>You define the real deliverables in your locale file.</i>

menu-debts =
    <b>What Svetlitsa handles in this example</b>

    ✅ Landing pages and simple sites
    ✅ Social visuals
    ✅ Light rebranding from scratch

    <b>Out of scope in the demo</b>

    ❌ Large enterprise engagements
    ❌ Legal services
    ❌ Paid ads managed end-to-end

menu-remote =
    The template targets a <b>remote-first</b> flow: Telegram bot, Fluent
    strings, form state in Redis — like a real service, with a made-up brand.

menu-docs =
    To get started in the example you only need a <b>short brief</b>: goal,
    audience, reference links. You can extend that for your own product.

    <i>Privacy policy is a separate document outside this template.</i>

btn-contact-lawyer = Open the form
btn-back = Back

contact-lawyer-message =
    Use the form below — it sends one tidy message to the admin chat.

form-q0 = Are you a private individual or a company?
form-individual = Individual
form-sole-proprietor = Company

form-q1 = Roughly what size is the task?
form-debt-up300 = Small scope
form-debt-300-500 = Medium project
form-debt-500-1m = Larger than average
form-debt-1m-plus = Complex / long-running
form-debt-exact = Discuss in chat

form-q2 = When would you like to start?
form-arrears-1m = Within a month
form-arrears-6m = In 1–3 months
form-arrears-1y = After six months
form-arrears-ontime = No fixed timeline yet

form-q3 =
    Thanks — answers saved.
    Send how to reach you: @username, phone, email, or any contact you prefer.

form-success =
    <b>All set!</b> We got your form. In production you can add your own
    response-time promise here.

form-admin-message =
    <b>New lead (Svetlitsa demo)</b>

    Client type: <code>{ $person_type }</code>
    Scope: <code>{ $debt }</code>
    Timeline: <code>{ $arrears }</code>
    Contact: <code>{ $contact }</code>
    On Telegram: { $user }
