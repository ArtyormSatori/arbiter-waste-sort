from typing import Dict, Any, List
from app.schemas import DisposalGuidance, PredictionItem

LABEL_RULES: Dict[str, Dict[str, Any]] = {
    "battery": {
        "category": "hazardous",
        "category_display": "Hazardous & E-Waste",
        "bin_name": "Orange / Red Drop-off (Hazardous Waste)",
        "bin_color_code": "#dc2626", # Red/Orange
        "bin_icon": "battery-alert",
        "detected_item": "Battery / Electrochemical Cell",
        "why_paragraph": (
            "Batteries contain concentrated heavy metals (such as lead, nickel, and cadmium) and volatile lithium-ion electrolytes that ignite violently under mechanical compression in collection trucks or sorting conveyors. They should NEVER be discarded in standard curbside trash or ordinary recycling bins, where they cause hundreds of municipal facility fires annually. Take spent batteries to dedicated battery drop-off kiosks, local electronics retailers, or municipal hazardous material collection depots."
        ),
        "preparation_tips": [
            "Tape the battery terminals with clear tape or electrical tape to prevent short circuits.",
            "Never puncture, crush, or disassemble damaged or swollen cells.",
            "Drop off at battery recycling kiosks located in supermarkets or municipal depots."
        ],
        "environmental_impact": "Prevents toxic heavy metal leaching into groundwater and eliminates a top fire hazard in waste collection vehicles."
    },
    "biological": {
        "category": "organic",
        "category_display": "Organic / Compostable",
        "bin_name": "Green Bin (Organics & Compost)",
        "bin_color_code": "#16a34a", # Green
        "bin_icon": "leaf",
        "detected_item": "Biodegradable Organic / Food Waste",
        "why_paragraph": (
            "Organic food scraps and biological plant materials are 100% biodegradable and nutrient-rich, but when trapped in anaerobic landfills without oxygen, they decompose into methane—a potent greenhouse gas with over 28 times the atmospheric warming potential of carbon dioxide. Separating organics into the green bin redirects them to industrial composting or anaerobic digestion facilities that produce organic fertilizer and biogas."
        ),
        "preparation_tips": [
            "Remove all plastic stickers, twist-ties, and rubber bands from fruit and vegetable matter.",
            "Do not bag in non-compostable plastic bags; use certified compostable liners or place loose in the green bin.",
            "Can also be added directly to backyard compost piles or vermicomposting bins."
        ],
        "environmental_impact": "Directly reduces landfill methane emissions and revitalizes depleted topsoil with natural organic matter."
    },
    "cardboard": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Blue Bin (Paper & Cardboard)",
        "bin_color_code": "#2563eb", # Blue
        "bin_icon": "package",
        "detected_item": "Corrugated Cardboard / Paperboard",
        "why_paragraph": (
            "Cardboard is manufactured from long virgin cellulose fibers that can be reclaimed and re-pulped up to 5 to 7 times into new packaging, saving 75% of the energy and water required to produce virgin paperboard. To avoid contaminating the paper recycling stream, the cardboard must remain clean and dry, free from heavy food oils, grease coatings, or food debris."
        ),
        "preparation_tips": [
            "Flatten and break down boxes completely to save volume in the collection truck.",
            "Remove plastic air pillows, polystyrene foam inserts, and excessive heavy packing tape.",
            "If heavily soiled with grease or food residues (such as greasy pizza box bottoms), tear off the soiled portion for the compost/trash and recycle only the clean top."
        ],
        "environmental_impact": "Conserves mature timber reserves, reduces pulping water consumption by 50%, and lowers paper production carbon footprint."
    },
    "paper": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Blue Bin (Paper & Cardboard)",
        "bin_color_code": "#2563eb", # Blue
        "bin_icon": "file-text",
        "detected_item": "Paper / Newspaper / Office Documents",
        "why_paragraph": (
            "Clean paper fibers are among the most readily recyclable commodities in municipal solid waste programs, converting directly back into paper towels, newsprint, and secondary stationery. Paper should be kept dry and segregated from wet food waste, as wet paper fibers disintegrate into slurry prematurely and clog automated optical sorting discs at materials recovery facilities (MRFs)."
        ),
        "preparation_tips": [
            "Ensure paper is clean and dry; do not recycle wax-coated, thermal receipt, or glitter-laminated paper.",
            "Small staples and envelope plastic address windows are acceptable and filtered during the re-pulping process.",
            "Place loose into the blue bin without plastic bagging."
        ],
        "environmental_impact": "Saves 17 trees, 7,000 gallons of water, and 4,000 kilowatt-hours of electrical energy per ton of recycled paper."
    },
    "metal": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Yellow / Blue Bin (Metals & Cans)",
        "bin_color_code": "#0284c7", # Light Blue / Cyan
        "bin_icon": "cylinder",
        "detected_item": "Metal / Aluminum / Tin Can",
        "why_paragraph": (
            "Metals such as aluminum beverage cans and tin-coated steel food cans are infinitely recyclable without any degradation in structural integrity or chemical purity. Recycling aluminum requires a staggering 95% less energy than mining and refining bauxite ore, making metal recovery one of the most economically and environmentally valuable components of the circular economy."
        ),
        "preparation_tips": [
            "Empty all remaining liquids and give the can a quick rinse to eliminate odors and insect attraction.",
            "Light crushing is acceptable to save bin space, but do not compress completely flat if your city uses optical sorting.",
            "Leave aluminum tabs attached to the can."
        ],
        "environmental_impact": "Recycling a single aluminum beverage can saves sufficient electricity to power a laptop for 3 hours or a TV for 2 hours."
    },
    "plastic": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Yellow / Blue Bin (Plastics)",
        "bin_color_code": "#0284c7", # Cyan
        "bin_icon": "recycle",
        "detected_item": "Rigid Plastic Container / Bottle",
        "why_paragraph": (
            "Rigid consumer plastics (principally PET #1 beverage bottles and HDPE #2 detergent jugs) can be washed, flaked, and remelted into recycled polyester fibers and new container preforms. However, thin plastic wraps, soft film bags, and food-contaminated plastics cannot be processed in standard curbside sorting lines and must be diverted to avoid jamming rotating mechanical sorters."
        ),
        "preparation_tips": [
            "Empty all liquid contents and rinse out food remnants.",
            "Screw the plastic cap tightly back onto the empty bottle (prevents caps from slipping through sorter screens).",
            "Do not bag recyclables in thin grocery bags; deposit loose into the recycling container."
        ],
        "environmental_impact": "Reduces petroleum extraction for virgin polymers and prevents microplastic leakage into marine and freshwater ecosystems."
    },
    "brown-glass": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Green / Blue Bin (Glass Recycling)",
        "bin_color_code": "#047857", # Emerald
        "bin_icon": "wine-bottle",
        "detected_item": "Amber / Brown Container Glass",
        "why_paragraph": (
            "Amber container glass, commonly used for beer and pharmaceutical bottles to shield light-sensitive contents from ultraviolet degradation, is 100% recyclable indefinitely. Cullet (crushed recycled glass) melts at significantly lower kiln temperatures than raw silica sand and soda ash, drastically cutting furnace greenhouse emissions."
        ),
        "preparation_tips": [
            "Rinse out residual beverage and remove crown bottle caps (recycle metal caps in the metal bin).",
            "Labels do not need to be scraped off; they burn off cleanly in the remelting furnace.",
            "Do not mix with heat-resistant borosilicate glassware (Pyrex), ceramics, mirrors, or window panes."
        ],
        "environmental_impact": "Every ton of glass recycled avoids 1.2 tons of virgin raw material extraction and cuts furnace CO2 emissions."
    },
    "green-glass": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Green / Blue Bin (Glass Recycling)",
        "bin_color_code": "#047857",
        "bin_icon": "wine-bottle",
        "detected_item": "Green Container Glass",
        "why_paragraph": (
            "Green container glass is formulated with iron and chromium oxides and can be recycled continuously into new green bottles and industrial fiberglass. Glass containers are inert and non-reactive, making recycled cullet a premium sustainable packaging medium that maintains food contact safety standards across unlimited recycling cycles."
        ),
        "preparation_tips": [
            "Empty contents and rinse clean.",
            "Remove corks or metal screw caps.",
            "Deposit carefully into the glass bin to minimize premature shattering before optical color sorting."
        ],
        "environmental_impact": "Reduces kiln operating temperatures by 30% and preserves pristine silica sand coastal reserves."
    },
    "white-glass": {
        "category": "recyclable",
        "category_display": "Recyclable",
        "bin_name": "Green / Blue Bin (Glass Recycling)",
        "bin_color_code": "#047857",
        "bin_icon": "wine-bottle",
        "detected_item": "Flint / Clear Container Glass",
        "why_paragraph": (
            "Clear flint glass jars and bottles represent the highest-value glass recycling stream because flint cullet can be re-manufactured into any colored glass or pristine clear containers. Mixing clear glass with ceramics, heat-resistant cookware, or crystal stemware containing lead ruins an entire furnace melt, so only standard packaging glass should enter the bin."
        ),
        "preparation_tips": [
            "Rinse clean to remove sauces or sticky food residues.",
            "Lids and metal rings should be separated into the metal recycling stream.",
            "Never deposit broken drinking glasses, porcelain dishes, or incandescent light bulbs here."
        ],
        "environmental_impact": "Zero material degradation over infinite cycles, conserving natural soda ash and limestone supplies."
    },
    "trash": {
        "category": "non-recyclable",
        "category_display": "Non-Recyclable (Landfill)",
        "bin_name": "Grey / Black Bin (General Residual Waste)",
        "bin_color_code": "#4b5563", # Grey
        "bin_icon": "trash-2",
        "detected_item": "Non-Recyclable Mixed / Contaminated Waste",
        "why_paragraph": (
            "This item consists of multi-layer composite materials, heavily contaminated packaging, or non-recyclable polymers that cannot be separated by standard municipal sorting technologies. Attempting to recycle items like soiled napkins, plastic wrap, or snack chip pouches ('wishcycling') contaminates good recyclables and increases processing overhead. Place this item into the grey or black landfill bin."
        ),
        "preparation_tips": [
            "Ensure the item is safely contained inside a sealed municipal trash bag.",
            "Check if any clean component (e.g. an outer paper sleeve) can be separated and recycled individually.",
            "For durable multi-material goods, explore local repair cafes or specialized mail-back programs."
        ],
        "environmental_impact": "Prevents batch contamination at materials recovery facilities, ensuring legitimate recyclables are not rejected into landfills."
    },
    "clothes": {
        "category": "non-recyclable",
        "category_display": "Textile / Donation Special Stream",
        "bin_name": "Purple Bin (Textile Donation) or Grey Bin",
        "bin_color_code": "#7c3aed", # Purple
        "bin_icon": "shirt",
        "detected_item": "Textiles / Fabric / Garment",
        "why_paragraph": (
            "Textiles and garments should NEVER be placed in curbside single-stream recycling bins because long fabrics and loose strings wrap around rotating trommels and conveyor bearings, halting MRF sorting lines. Clean, wearable clothes should be donated to secondhand organizations or dedicated textile donation bins; unwearable stained fabric should go to specialized rag upcycling or residual general waste."
        ),
        "preparation_tips": [
            "If in wearable condition, donate to local thrift shops, shelters, or clothing drop-off boxes.",
            "Wash and dry textiles before donation to prevent mold growth in collection bins.",
            "If severely damaged or oil-soaked, discard in the grey general waste bin."
        ],
        "environmental_impact": "Extending garment life by just 9 months reduces carbon, waste, and water footprints by approximately 20-30%."
    },
    "shoes": {
        "category": "non-recyclable",
        "category_display": "Footwear / Donation Special Stream",
        "bin_name": "Purple Bin (Donation) or Grey Bin (General Waste)",
        "bin_color_code": "#7c3aed",
        "bin_icon": "footprints",
        "detected_item": "Footwear / Shoes",
        "why_paragraph": (
            "Footwear consists of tightly bonded composite layers of vulcanized rubber, EVA foam, leather, adhesives, and textiles that cannot be mechanically separated in municipal curbside recycling facilities. Shoes in good repair should be donated to charity or deposited in athletic brand shoe-grinding take-back bins for playground turf repurposing; otherwise, place them in the residual grey waste bin."
        ),
        "preparation_tips": [
            "Tie pairs together by the laces to prevent separation during donation collection.",
            "Look for athletic shoe recycling bins (e.g., Nike Grind) at sports retailers.",
            "If completely disintegrated or hazardous, discard in the grey landfill bin."
        ],
        "environmental_impact": "Directs reusable footwear to communities in need and keeps vulcanized rubber out of overburdened landfills."
    }
}

# Generic fallback for any unlisted or custom label
DEFAULT_FALLBACK: Dict[str, Any] = {
    "category": "non-recyclable",
    "category_display": "Non-Recyclable (Landfill)",
    "bin_name": "Grey / Black Bin (General Residual Waste)",
    "bin_color_code": "#4b5563",
    "bin_icon": "trash-2",
    "detected_item": "Unclassified Solid Waste",
    "why_paragraph": (
        "This item does not match verified high-grade curbside recycling specifications or clean compostable streams. When in doubt, disposing of unverified items in the general residual waste bin protects the municipal recycling stream from contamination that could cause entire bales of recoverable materials to be rejected."
    ),
    "preparation_tips": [
        "Check municipal packaging labels for regional disposal symbols.",
        "When in doubt, dispose in general trash to prevent recycling stream contamination."
    ],
    "environmental_impact": "Protects municipal recycling purity and prevents processing line shutdowns."
}

def resolve_disposal_guidance(label: str, score: float) -> DisposalGuidance:
    norm_label = label.lower().strip()
    rule = LABEL_RULES.get(norm_label, DEFAULT_FALLBACK)
    return DisposalGuidance(
        category=rule["category"],
        category_display=rule["category_display"],
        bin_name=rule["bin_name"],
        bin_color_code=rule["bin_color_code"],
        bin_icon=rule["bin_icon"],
        confidence=round(score, 4),
        detected_item=rule["detected_item"],
        why_paragraph=rule["why_paragraph"],
        preparation_tips=rule["preparation_tips"],
        environmental_impact=rule["environmental_impact"]
    )

def map_predictions(raw_predictions: List[Dict[str, Any]]) -> List[PredictionItem]:
    items = []
    for p in raw_predictions:
        lbl = p.get("label", "").lower().strip()
        sc = float(p.get("score", 0.0))
        rule = LABEL_RULES.get(lbl, DEFAULT_FALLBACK)
        items.append(PredictionItem(
            label=lbl,
            score=round(sc, 4),
            category=rule["category"],
            bin_name=rule["bin_name"]
        ))
    return items
