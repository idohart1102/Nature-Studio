# Sổ nguồn — Redfish / red drum

Hồ sơ: [redfish](../../species/redfish.md). Cấp nguồn và quy tắc truy cập theo [chuẩn hồ sơ loài](../../../00-Standards/species-profile-standard.md). Nghiên cứu lại 2026-10-25: R1/R2 của bản v2.1 nay là S6/S7. Bản v2.1 ghi R1 hỗ trợ "biến thiên đốm" và "cá lớn 5 ft"; mở trực tiếp cho thấy S6 chỉ nêu một đốm lớn, con số 5 ft nằm ở S7. Hồ sơ v3 đã sửa trích dẫn. Bổ sung 2026-10-25 (v3.1): lịch mùa từ S6, S9, S11 (mở lại) và S14 (ASMFC, mới).

Chưa truy cập được: MyFWC (HTTP 403), SRAC fact sheet 320 (PDF không đọc được văn bản), Georgia DNR Coastal (403), trang red drum của NOAA Fisheries và NC DMF (404 tại URL đã thử).

```json
{
 "species_id": "K-SP-REDFISH-001",
 "sources": [
  {
   "id": "S1",
   "tier": "A",
   "title": "ITIS Standard Report: Sciaenops ocellatus, TSN 169290",
   "publisher": "ITIS",
   "url": "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=169290",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "valid name, authority (Linnaeus, 1766), family Sciaenidae; ITIS still places it in Perciformes",
   "limits": "Order follows older scheme"
  },
  {
   "id": "S2",
   "tier": "A",
   "title": "WoRMS: Sciaenops ocellatus, AphiaID 159335",
   "publisher": "World Register of Marine Species",
   "url": "https://www.marinespecies.org/aphia.php?p=taxlist&tName=Sciaenops%20ocellatus",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "authority; Eupercaria incertae sedis > Sciaenidae",
   "limits": ""
  },
  {
   "id": "S3",
   "tier": "A",
   "title": "Eschmeyer's Catalog of Fishes: Species by Family",
   "publisher": "California Academy of Sciences",
   "url": "https://researcharchive.calacademy.org/research/ichthyology/catalog/SpeciesByFamily.asp",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "Sciaenidae placed in Acanthuriformes",
   "limits": ""
  },
  {
   "id": "S4",
   "tier": "A",
   "title": "FishBase summary: Sciaenops ocellatus",
   "publisher": "FishBase",
   "url": "https://www.fishbase.se/summary/Sciaenops-ocellatus.html",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "common length 100 cm TL, max 155 cm TL, max weight 45 kg, max age 50 y, length-weight a=0.00851 b=3.07, range, habitat",
   "limits": "Length-weight is a Bayesian estimate; Lm range printed inconsistently; depth range 10-? m"
  },
  {
   "id": "S5",
   "tier": "A",
   "title": "FishBase common names: Sciaenops ocellatus",
   "publisher": "FishBase",
   "url": "https://www.fishbase.se/ComNames/CommonNamesList.php?ID=1191",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "English names channel bass, red drum, redfish, spotted bass; no Vietnamese name listed",
   "limits": ""
  },
  {
   "id": "S6",
   "tier": "B",
   "title": "Red Drum (Sciaenops ocellatus)",
   "publisher": "Texas Parks and Wildlife Department",
   "url": "https://tpwd.texas.gov/huntwild/wild/species/reddrum/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "one large tail-base spot, colour range, tailing, fresh-water tolerance, spawning mid-Aug to mid-Oct, drumming, growth years 1-3, predators, line test 8-15/17-25/25-40 lb; winter concentrations in rivers and tidal creeks; fall movement of large adults to Gulf beaches especially in stormy weather (bull redfish run); surf/pier rods over 10 ft for bull reds; natural bait best for bull reds",
   "limits": "Does not mention multiple spots; seasons given as winter/fall without months"
  },
  {
   "id": "S7",
   "tier": "B",
   "title": "Redfish, an angler's delight",
   "publisher": "Texas Parks and Wildlife Department",
   "url": "https://tpwd.texas.gov/fishboat/fish/didyouknow/coastal/reddrum.phtml",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "five feet / 80+ lb large fish, Texas average 23 in, larva/juvenile size, age 1-2 growth, maturity, world record month, Texas record",
   "limits": "Historical article; records may be superseded"
  },
  {
   "id": "S8",
   "tier": "B",
   "title": "North Carolina State Saltwater Records",
   "publisher": "NC DEQ Division of Marine Fisheries",
   "url": "https://deq.nc.gov/about/divisions/marine-fisheries/public-information-and-education/coastal-fishing-information/nc-saltwater-fishing-tournament/north-carolina-state-saltwater-records",
   "published": "2026-09-01",
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "94 lb 2 oz, Hatteras Island 1984, world all-tackle record",
   "limits": "Publication date taken from data export name"
  },
  {
   "id": "S9",
   "tier": "B",
   "title": "Marine Species: Red Drum",
   "publisher": "South Carolina Department of Natural Resources",
   "url": "https://dnr.sc.gov/marine/species/reddrum.html",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "one or more spots, SC average 18 in, maturity by sex, age 38 y, juvenile marsh-edge habitat, diet by stage, nearshore groups, spawning near inlets",
   "limits": ""
  },
  {
   "id": "S10",
   "tier": "B",
   "title": "Black Drum (Pogonias cromis)",
   "publisher": "Texas Parks and Wildlife Department",
   "url": "https://tpwd.texas.gov/huntwild/wild/species/blackdrum/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "look-alike: barbels under jaw, high back, juvenile vertical bars",
   "limits": ""
  },
  {
   "id": "S11",
   "tier": "C",
   "title": "Discover Fishes: Sciaenops ocellatus",
   "publisher": "Florida Museum of Natural History",
   "url": "https://www.floridamuseum.ufl.edu/discover-fish/species-profiles/sciaenops-ocellatus/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "several spots in some fish, body shape, no barbels, salinity 30-35 ppt, schooling, spot may misdirect predators; common names incl. bull red, puppy drum, rat red; spawning mid-August to mid-November near tidal inlets",
   "limits": ""
  },
  {
   "id": "S12",
   "tier": "A",
   "title": "IUCN Red List: Sciaenops ocellatus (as cited by FishBase)",
   "publisher": "IUCN",
   "url": "https://www.iucnredlist.org/",
   "published": "2020-01-24",
   "accessed": "2026-10-25",
   "access": "indexed-only",
   "supports": "Least Concern, assessed 2020-01-24",
   "limits": "IUCN page itself not opened"
  },
  {
   "id": "S13",
   "tier": "E",
   "title": "Angler media on the 1984 world record",
   "publisher": "sportfishingmag.com, fishgame.com",
   "url": "https://www.sportfishingmag.com/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "indexed-only",
   "supports": "lead only: 7 Nov 1984, Avon surf, 57 in fork length",
   "limits": "Tier E, not a fact source"
  },
  {
   "id": "S14",
   "tier": "B",
   "title": "Red Drum (species page)",
   "publisher": "Atlantic States Marine Fisheries Commission",
   "url": "https://asmfc.org/species/red-drum/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "Atlantic adults move offshore or south in winter and inshore or north in spring; spawning at night in nearshore waters during summer and fall; eggs hatch in 24-36 h; larvae carried into estuarine nurseries",
   "limits": "Atlantic coast only; seasons without months"
  },
  {
   "id": "S15",
   "tier": "B",
   "title": "Bait Use 101 (Did You Know? coastal short report)",
   "publisher": "Texas Parks and Wildlife Department",
   "url": "https://tpwd.texas.gov/fishboat/fish/didyouknow/coastal/baituse101.phtml",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "live shrimp is the bait of choice for Texas marine sportfish incl. red drum; few red drum turn down a live finger mullet; soft plastics (shrimp tails, shad tails, paddle tails) are the top artificial lure for Texas inshore fish incl. red drum",
   "limits": "outreach article; catch shares are Texas private-boat survey figures from 2006; no hooking instructions"
  },
  {
   "id": "S16",
   "tier": "B",
   "title": "Learn to Fish: A Basic Guide for the Beginning Angler (PWD BK K0700-0639d), p. 16 Natural and live baits",
   "publisher": "Texas Parks and Wildlife Department",
   "url": "https://tpwd.texas.gov/publications/pwdpubs/media/pwd_bk_k0700_0639d.pdf",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "crabs used as bait to catch red drum (with sheepshead, black drum, cobia, snapper)",
   "limits": "beginner guide; no sizes; Texas licence note elsewhere"
  }
 ]
}
```
