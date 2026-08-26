from urllib.parse import quote

from flask import Flask, abort, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = "chubby-properties-local-development-key"

WHATSAPP_NUMBER = "2348112835788"
WHATSAPP_DISPLAY = "+234 811 283 5788"

PROPERTIES = {
    "farmland-abam-abia": {
        "slug": "farmland-abam-abia",
        "title": "300 Plots of Farmland for Sale in Abam, Abia State",
        "short_title": "300 Plots of Farmland for Sale in Abam, Abia State",
        "location": "Abam, Abia State, Nigeria",
        "price": "₦300,000 / Plot",
        "availability": "300 Plots Available",
        "category": "Land / Farmland",
        "listing_type": "For Sale",
        "image": "property-farmland.jpg",
        "image_alt": "Illustrated farmland and palm plantation placeholder for the Abam, Abia State property",
        "eyebrow": "LAND OPPORTUNITY",
        "overview": "A farmland opportunity in Abam, Abia State, presented for buyers seeking land in the Nigerian market.",
        "description": "This listing comprises 300 plots of farmland available for sale in Abam, Abia State. The quoted price is stated per plot, so buyers can enquire about the portion that best fits their plans.",
        "location_note": "The property is located in Abam, Abia State, Nigeria. Contact Chubby Properties for availability, viewing information, documentation guidance, and next steps.",
        "enquiry": "Hello Chubby Properties, I am interested in the 300 plots of farmland for sale in Abam, Abia State. I would like more information.",
    },
    "uncompleted-2-storey-building-ahiaeke-ibeku": {
        "slug": "uncompleted-2-storey-building-ahiaeke-ibeku",
        "title": "Uncompleted 2-Storey Building for Sale in Ahiaeke Ibeku, Umuahia",
        "short_title": "Uncompleted 2-Storey Building for Sale in Ahiaeke Ibeku, Umuahia",
        "location": "Ahiaeke Ibeku, Umuahia, Abia State, Nigeria",
        "price": "₦80,000,000",
        "availability": None,
        "category": "Building / Property",
        "listing_type": "For Sale",
        "image": "property-building.jpg",
        "image_alt": "Illustrated uncompleted two-storey building placeholder for the Ahiaeke Ibeku property",
        "eyebrow": "DEVELOPMENT OPPORTUNITY",
        "overview": "An uncompleted 2-storey building available for sale in Ahiaeke Ibeku, Umuahia, Abia State.",
        "description": "This property is an uncompleted 2-storey building offered for sale. The listing is intentionally presented with only the information supplied; enquire directly for further details and to arrange the appropriate next conversation.",
        "location_note": "The property is located in Ahiaeke Ibeku, Umuahia, Abia State, Nigeria. Chubby Properties can guide interested buyers through the enquiry and viewing process.",
        "enquiry": "Hello Chubby Properties, I am interested in the uncompleted 2-storey building for sale in Ahiaeke Ibeku, Umuahia. I would like more information.",
    },
}

SERVICES = [
    {
        "icon": "compass",
        "title": "Real Estate Consultancy",
        "description": "Professional guidance for individuals and businesses navigating property decisions across Nigeria.",
    },
    {
        "icon": "key-round",
        "title": "Property Management",
        "description": "Practical support for managing property interests with clarity, care, and accountability.",
    },
    {
        "icon": "arrow-left-right",
        "title": "Buying & Selling of Properties",
        "description": "A client-focused approach to connecting people with property opportunities and transactions.",
    },
    {
        "icon": "trending-up",
        "title": "Real Estate Investment Advisory",
        "description": "Clearer thinking around real estate opportunities, value creation, and long-term decisions.",
    },
    {
        "icon": "file-check-2",
        "title": "Property Valuation & Documentation Support",
        "description": "Support with understanding property value and the documentation steps involved in a transaction.",
    },
]

WHY_CHOOSE_US = [
    {
        "icon": "map",
        "title": "Nigerian Market Expertise",
        "description": "Context-aware guidance for property decisions in the Nigerian market.",
    },
    {
        "icon": "eye",
        "title": "Transparent & Client-Focused Service",
        "description": "Straightforward communication that keeps your goals at the centre of the conversation.",
    },
    {
        "icon": "globe-2",
        "title": "Nationwide Property Solutions",
        "description": "Property consultancy and management solutions for clients across all states in Nigeria.",
    },
    {
        "icon": "handshake",
        "title": "Professional Guidance",
        "description": "A considered, step-by-step approach from first enquiry to informed action.",
    },
    {
        "icon": "badge-check",
        "title": "Commitment to Excellence & Integrity",
        "description": "A commitment to delivering careful service and building lasting relationships.",
    },
]


def whatsapp_url(message: str) -> str:
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"


def property_context(property_item: dict) -> dict:
    item = dict(property_item)
    item["whatsapp_url"] = whatsapp_url(item["enquiry"])
    return item


@app.context_processor
def inject_globals():
    return {
        "whatsapp_display": WHATSAPP_DISPLAY,
        "whatsapp_url": whatsapp_url("Hello Chubby Properties, I would like to speak with an agent about available properties."),
        "current_year": 2026,
    }


@app.route("/")
def home():
    featured = [property_context(PROPERTIES["farmland-abam-abia"]), property_context(PROPERTIES["uncompleted-2-storey-building-ahiaeke-ibeku"])]
    return render_template(
        "home.html",
        title="Premium Real Estate Consultancy Across Nigeria",
        meta_description="Chubby Property Development Ltd helps individuals and businesses buy, sell, manage, and invest in property across Nigeria.",
        featured=featured,
        services=SERVICES,
        why_choose_us=WHY_CHOOSE_US,
    )


@app.route("/properties")
def properties():
    listings = [property_context(item) for item in PROPERTIES.values()]
    return render_template(
        "properties.html",
        title="Properties for Sale Across Nigeria",
        meta_description="Explore selected land and property opportunities presented by Chubby Property Development Ltd.",
        properties=listings,
    )


@app.route("/properties/<slug>")
def property_detail(slug):
    property_item = PROPERTIES.get(slug)
    if not property_item:
        abort(404)
    related = [property_context(item) for key, item in PROPERTIES.items() if key != slug]
    return render_template(
        "property_detail.html",
        title=property_item["title"],
        meta_description=f"{property_item['title']} — enquire with Chubby Property Development Ltd for more information.",
        property=property_context(property_item),
        related=related,
    )


@app.route("/about")
def about():
    return render_template(
        "about.html",
        title="About Chubby Property Development Ltd",
        meta_description="Learn about Chubby Property Development Ltd, a trusted real estate consultancy and property management company operating across Nigeria.",
        why_choose_us=WHY_CHOOSE_US,
    )


@app.route("/services")
def services():
    return render_template(
        "services.html",
        title="Real Estate Services Across Nigeria",
        meta_description="Explore real estate consultancy, property management, buying and selling, investment advisory, and documentation support.",
        services=SERVICES,
    )


@app.route("/sell-with-us", methods=["GET", "POST"])
def sell_with_us():
    if request.method == "POST":
        form = request.form
        message = (
            "Hello Chubby Properties, I would like to list my property for sale.\n\n"
            f"Name: {form.get('full_name', '').strip()}\n"
            f"Phone: {form.get('phone', '').strip()}\n"
            f"Property Type: {form.get('property_type', '').strip()}\n"
            f"Location: {form.get('location', '').strip()}\n"
            f"Asking Price: {form.get('asking_price', '').strip()}\n"
            f"Description: {form.get('description', '').strip()}"
        )
        return redirect(whatsapp_url(message))
    return render_template(
        "sell_with_us.html",
        title="Sell Your Property With Chubby Properties",
        meta_description="Share your property details with Chubby Property Development Ltd and continue the conversation on WhatsApp.",
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        form = request.form
        message = (
            "Hello Chubby Properties, I would like to make an enquiry.\n\n"
            f"Name: {form.get('full_name', '').strip()}\n"
            f"Phone: {form.get('phone', '').strip()}\n"
            f"Enquiry: {form.get('message', '').strip()}"
        )
        return redirect(whatsapp_url(message))
    return render_template(
        "contact.html",
        title="Contact Chubby Property Development Ltd",
        meta_description="Talk with Chubby Property Development Ltd about property buying, selling, management, and investment opportunities in Nigeria.",
    )


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", title="Page Not Found", meta_description="The requested page could not be found."), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
