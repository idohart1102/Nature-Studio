# Sổ nguồn — Mahi-mahi / common dolphinfish

Hồ sơ: [mahi-mahi](../../species/mahi-mahi.md). Cấp nguồn và quy tắc truy cập theo [chuẩn hồ sơ loài](../../../00-Standards/species-profile-standard.md). Nghiên cứu 2026-10-25.

Mâu thuẫn đã ghi: NOAA (S5) và SAFMC (S6) viết mahi có "tooth patch trên lưỡi rất rộng, vuông"; FishBase (S3, S9) và Florida Museum (S4) ghi ngược lại: mahi có mảng răng lưỡi nhỏ, bầu dục, còn pompano dolphinfish mới có mảng rộng, vuông. Hồ sơ theo S3/S4/S9 và không dùng dấu này cho kiểm ảnh.

Chưa truy cập được: MyFWC (HTTP 403 cho trang dolphin), bài gốc Merten et al. 2022 (chỉ đọc qua tóm tắt S8).

```json
{
 "species_id": "K-SP-MAHI-MAHI-001",
 "sources": [
  {
   "id": "S1",
   "tier": "A",
   "title": "ITIS: Coryphaena hippurus, TSN 168791",
   "publisher": "ITIS",
   "url": "https://www.itis.gov/servlet/SingleRpt/SingleRpt?search_topic=TSN&search_value=168791",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "valid name, authority Linnaeus, 1758; ITIS hierarchy Perciformes > Coryphaenidae",
   "limits": "Read through the ITIS JSON web service (searchByScientificName, getFullHierarchyFromTSN), not the HTML report page; order follows older scheme"
  },
  {
   "id": "S2",
   "tier": "A",
   "title": "WoRMS: Coryphaena hippurus, AphiaID 126846",
   "publisher": "World Register of Marine Species",
   "url": "https://www.marinespecies.org/aphia.php?p=taxdetails&id=126846",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "accepted name, authority Linnaeus, 1758; Carangiformes > Coryphaenidae",
   "limits": "Read through the WoRMS REST API record, not the HTML page"
  },
  {
   "id": "S3",
   "tier": "A",
   "title": "FishBase summary: Coryphaena hippurus",
   "publisher": "FishBase",
   "url": "https://www.fishbase.se/summary/Coryphaena-hippurus.html",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "Carangiformes > Coryphaenidae; common length 100 cm TL, max 210 cm TL, max weight 40 kg, max age 4 y, Lm 55.8 cm; depth 0-85 m usually 5-10 m, 21-30 C; male bony head crest; body depth <25% SL; small oval tongue tooth patch; 58-66 dorsal rays; concave anal fin; colour in life and grey with green tinge after death; juvenile caudal tips white, pelvic fins black; schools; diet; trolling/longline; IUCN LC 2010 as cited",
   "limits": "Aggregated database; Lm and length figures not split by sex"
  },
  {
   "id": "S4",
   "tier": "C",
   "title": "Discover Fishes: Coryphaena hippurus",
   "publisher": "Florida Museum of Natural History",
   "url": "https://www.floridamuseum.ufl.edu/discover-fish/species-profiles/coryphaena-hippurus/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "common 3 ft / 30 lb, max 6 ft, Florida record 77 lb 12 oz, world record 87 lb; colour, rapid fade to silver after capture; juvenile bars at 10-20 mm, fade with growth; juvenile caudal and pelvic marks vs pompano; male bony ridge; schools of small fish, large fish alone or in pairs; Sargassum and floating objects; diet by stage, flyingfish ~25% by weight; day feeding; predators; spawning in pairs, year-round in tropics, young in Florida Current year-round with summer peak; larval sizes; maturity ~8 in at 4-5 months",
   "limits": "Undated web profile; records may be superseded"
  },
  {
   "id": "S5",
   "tier": "B",
   "title": "Atlantic Mahi Mahi (FishWatch species page)",
   "publisher": "NOAA Fisheries",
   "url": "https://www.fisheries.noaa.gov/species/atlantic-mahi-mahi",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "colour, fades almost immediately after harvest; adult males square head, females rounded head; up to almost 7 ft and 88 lb; lifespan up to 5 y; mature at 4-5 months; spawning under Sargassum; diet and predators; juveniles school, older fish usually alone; larger males prefer open ocean, females and smaller males near floating objects; range Massachusetts to Texas; uses 'bull' and 'cow' for males and females in a photo caption",
   "limits": "Tongue tooth-patch statement conflicts with S3/S4/S9 (see header)"
  },
  {
   "id": "S6",
   "tier": "B",
   "title": "Dolphin (species page)",
   "publisher": "South Atlantic Fishery Management Council",
   "url": "https://safmc.net/species/dolphin/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "colour fades almost immediately upon death; adult male head profile nearly vertical, female more sloping; average FL 34-55 in; spawning Florida Current Nov-Jul, Gulf Stream off NC June-July; Sargassum association; speed estimated 50 knots; recreational bag 10/person/day, vessel 54, 20 in FL minimum off FL/GA/SC",
   "limits": "Same tooth-patch conflict as S5; regulations change, read on 2026-10-25"
  },
  {
   "id": "S7",
   "tier": "B",
   "title": "North Carolina State Saltwater Records",
   "publisher": "NC DEQ Division of Marine Fisheries",
   "url": "https://deq.nc.gov/about/divisions/marine-fisheries/public-information-and-education/coastal-fishing-information/nc-saltwater-fishing-tournament/north-carolina-state-saltwater-records",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "NC record dolphin 79 lb 0 oz, Cape Hatteras 1993; pompano dolphinfish 11 lb 5.4 oz, off Ocean Isle Beach 2022",
   "limits": ""
  },
  {
   "id": "S8",
   "tier": "C",
   "title": "Where Do Dolphinfish Roam? (Hook, Line & Science)",
   "publisher": "North Carolina Sea Grant",
   "url": "https://ncseagrant.ncsu.edu/hooklinescience/where-do-dolphinfish-roam/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "summary of Merten et al. 2022: 23,232 tagged 2002-2017, most tagged fish 18-22 in FL, average northward movement Florida to Mid-Atlantic Bight in 44 days, fastest Florida-NC 7 days, 71% recaptured within 40 days",
   "limits": "Secondary summary of a peer-reviewed paper; no month-by-month timing"
  },
  {
   "id": "S9",
   "tier": "A",
   "title": "FishBase summary: Coryphaena equiselis",
   "publisher": "FishBase",
   "url": "https://www.fishbase.se/summary/Coryphaena-equiselis.html",
   "published": null,
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "look-alike: body depth >25% SL, broad square tongue tooth patch, 52-59 dorsal rays, convex anal fin, juvenile caudal margin entirely white, crest develops in large adults of both sexes but more in males; common 50 cm TL, max 146 cm TL",
   "limits": ""
  },
  {
   "id": "S10",
   "tier": "E",
   "title": "Angler media on East Coast dolphin timing (Dolphinfish Research Program interviews)",
   "publisher": "sportfishingmag.com, saltwatersportsman.com",
   "url": "https://www.sportfishingmag.com/",
   "published": null,
   "accessed": "2026-10-25",
   "access": "indexed-only",
   "supports": "lead only: first fish off South Carolina around late April, Outer Banks early May, Mid-Atlantic Bight mid-June to late September; Florida Keys peak late May-July",
   "limits": "Tier E, seen only in search snippets; not a fact source"
  },
  {
   "id": "S11",
   "tier": "B",
   "title": "Fishery Management Plan for the Dolphin and Wahoo Fishery of the Atlantic (January 2003), Appendix F (PDF pp. 515, 536)",
   "publisher": "South Atlantic Fishery Management Council",
   "url": "https://safmc.net/documents/dolphin-wahoo-fishery-management-plan/",
   "published": "2003-01",
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "dolphin primarily caught by trolling live or artificial bait near a floating object or floating material such as grass or a weedline; a hooked fish is often left in the water to hold the school, chunks of bait are tossed and fish are hooked as the school rises; anglers also cast into a school amid bait chunks; charter vessels troll about 4.5-6 knots; trolling for dolphin and wahoo at 4-10 knots near or through weedlines",
   "limits": "2003 description; data said to be scant; no lure types named"
  },
  {
   "id": "S12",
   "tier": "B",
   "title": "Maryland Weekly Fishing Report, July 8, 2015",
   "publisher": "Maryland Department of Natural Resources",
   "url": "https://dnrweb.dnr.state.md.us/fisheries/fishingreport/index.asp?d=07082015",
   "published": "2015-07-08",
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "dolphin (with yellowfin and bluefin) caught along the 30-fathom line by boats trolling a mixed spread of lures and rigged ballyhoo",
   "limits": "one weekly report"
  },
  {
   "id": "S13",
   "tier": "B",
   "title": "Maryland Weekly Fishing Report, July 22, 2015",
   "publisher": "Maryland Department of Natural Resources",
   "url": "https://dnrweb.dnr.state.md.us/fisheries/fishingreport/index.asp?d=07222015",
   "published": "2015-07-22",
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "small 'chicken' dolphin attracted to the shade of head boats, caught by drifting bait to them",
   "limits": "one weekly report; bait type not named"
  },
  {
   "id": "S14",
   "tier": "B",
   "title": "Maryland Weekly Fishing Report, September 9, 2015",
   "publisher": "Maryland Department of Natural Resources",
   "url": "https://dnrweb.dnr.state.md.us/fisheries/fishingreport/index.asp?d=09092015",
   "published": "2015-09-09",
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "dolphin very plentiful along weed lines and lobster-pot buoys, some gaffer-sized",
   "limits": "one weekly report"
  },
  {
   "id": "S15",
   "tier": "A",
   "title": "McBride, Foushee & Mahmoudi (1996) Florida's halfbeak, Hemiramphus spp., bait fishery. Marine Fisheries Review 58(1-2):29-38",
   "publisher": "NOAA National Marine Fisheries Service",
   "url": "https://spo.nmfs.noaa.gov/sites/default/files/pdf-content/MFR/mfr581-2/mfr581-24.pdf",
   "published": "1996",
   "accessed": "2026-10-25",
   "access": "opened",
   "supports": "halfbeaks (ballyhoo, balao) are frequently the preferred bait for anglers seeking billfishes, dolphin (Coryphaena hippurus), groupers; larger sizes used for trolling for offshore pelagic gamefishes",
   "limits": "Florida fishery; cites older literature for the preference"
  }
 ]
}
```
