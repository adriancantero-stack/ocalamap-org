import re
import json
import random

raw_data = """
CATEGORIA 1 — ACTIVITIES
ATV
1. ATV Off-Road Adventure Tours
Tours in Ocala National Forest by Appt.
📞 (352) 546-5514
🌐 www.ATVOffRoadAdventureTours.com

AMUSEMENTS
1. Belleview Cinemas
10845 SE US Hwy. 441, Belleview
📞 (352) 245-7015
2. Chuck E. Cheese
3500 SW College Rd., #200, Ocala
📞 (352) 622-6357
3. Easy Street Family Fun Center
2727 SW 27th Ave., Ocala
📞 (352) 861-9700
🌐 www.FunWorks.com/EasyStreet
4. Marion Theatre
50 S. Magnolia Ave., Ocala
📞 (352) 629-6300
🌐 www.MarionTheatre.org
5. Ocala Center 6
2021 Silver Springs Blvd., Ocala
📞 (352) 624-8798
6. Ocala Drive-in
4850 S. Pine Ave., Ocala
📞 (352) 629-1325
🌐 www.OcalaDriveIn.info
7. Ocala Gran Prix
4121 NW 44th Ave., Ocala
📞 (352) 291-0600
🌐 www.OcalaGranPrix.com
8. Painting With A Twist
4414 SW College Rd., Ocala
📞 (352) 368-7928
🌐 www.PaintingWithATwist.com/Ocala
9. Picasso’s Palette
106 SW 17th St., Ocala
📞 (352) 789-6670
🌐 www.PicassosPalette.com
10. Regal Hollywood 16
2801 SW 27th Ave., Ocala
📞 (352) 861-2699
11. Skate-A-Way South
2008 E. Silver Springs Blvd., Ocala
📞 (352) 672-8100
🌐 www.SkateAWaySouth.com
12. Skate Mania
5461 SE Maricamp Rd., Ocala
📞 (352) 624-4222
🌐 www.SkateMania.org
13. Wayne’s World of Paintball
4841 S. Pine Ave., Ocala
📞 (352) 401-1801
🌐 www.Waynes-World.com

ATTRACTIONS
1. Silver Springs State Park
5656 E. Silver Springs Blvd., Silver Springs
📞 (352) 236-7148
🌐 www.SilverSprings.com
2. Wild Waters
5656 E. Silver Springs Blvd., Silver Springs
📞 (352) 877-2267
🌐 www.SilverSprings.com/wild-waters

BOWLING ALLEYS
1. AMF Galaxy East Lanes
3225 SE Maricamp Rd., Ocala
📞 (352) 694-1111
🌐 www.AMF.com/GalaxyEastLanes
2. AMF Galaxy West Lanes
1818 SW 17th St., Ocala
📞 (352) 732-0300
🌐 www.AMF.com/GalaxyWestLanes

DIVING
1. 40 Fathom Grotto
9487 NW 115th Ave., Ocala
📞 (352) 368-7974
🌐 www.40FathomGrotto.com

FLEA MARKETS
1. Grumpy Jerry’s
12180 SE 122nd Lane, Belleview
📞 (352) 245-3532
🌐 www.GrumpyJerrysFleaMarket.com
2. I-75 Super Flea Market
4121 NW 44th Ave., Ocala
📞 (352) 351-9220
🌐 www.I75SuperFlea.com
3. The Market of Marion
12888 SE US Hwy. 441, Belleview
📞 (352) 245-6766
🌐 www.TheMarketOfMarion.com

GOLF COURSES / DRIVING RANGES
1. Baseline Golf Course & Lighted Driving Range
4255 SE 58th Ave., Ocala
📞 (352) 624-9990
🌐 www.BaselineGolfCourse.com
2. Candler Hills Golf & Practice Facility
8137 SW 90th Terrace Rd., Ocala
📞 (352) 861-9712
🌐 www.CandlerHillsGolfClub.com
3. Country Club at Silver Springs Shores
633 Silver Rd., Silver Springs
📞 (352) 687-2828
🌐 www.SilverSpringsGolfCC.com
4. Del Web Spruce Creek Eagle Ridge Golf Club
13605 Del Webb Blvd., Summerfield
📞 (352) 307-1668
🌐 www.PlayEagleRidgeGolf.com
5. Grand Lake RV & Golf Resort
18545 NW 45th Avenue Rd., Citra
📞 (888) 484-4720
🌐 www.GrandLakeResort.com
6. Huntington Golf Club
799 Marion Oaks Manor, Ocala
📞 (352) 347-3333
🌐 www.HuntingtonGolfClub.com
7. Juliette Falls
6933 SW 179th Ave Rd., Dunnellon
📞 (352) 522-0309
🌐 www.JulietteFalls.com
8. Lake Diamond Golf & Country Club
16 Golf View Dr., Ocala
📞 (352) 687-1000
9. Marion Oaks Golf & Country Club
430 Marion Oaks Golf Way, Ocala
📞 (352) 347-1271
🌐 www.MarionOaksCountryClub.com
10. Mellex Golf Center
6875 SW Hwy. 200, Ocala
📞 (352) 789-0841
11. Ocala Golf Club
3130 E. Silver Springs Blvd., Ocala
📞 (352) 401-6917
🌐 www.OcalaGolfClub.com
12. Ocala National Golf Club
4782 NW 80th Ave., Ocala
📞 (352) 629-7981
🌐 www.OcalaNational.com


CATEGORIA 2 — ARTS & CULTURE
CONCERTS
1. Circle Square Cultural Center at On Top of the World
8395 SW 80th St., Ocala
📞 (352) 854-3670
🌐 www.CSCulturalCenter.com
2. Citizen’s Circle “Feel Downtown Live”
151 SE Osceola Ave., Ocala
📞 (352) 401-3980
🌐 www.FeelDowntownOcala.com
3. Orange Blossom Opry
16439 SE Hwy. 42, Weirsdale
📞 (352) 821-1201
🌐 www.OB0pry.com

MUSEUMS / GALLERIES
1. Appleton Museum of Art
4333 E. Silver Springs Blvd., Ocala
📞 (352) 291-4455
🌐 www.AppletonMuseum.org
2. Brick City Center for the Arts
23 SW Broadway, Ocala
📞 (352) 369-1500
🌐 www.MCAOcala.com
3. My Discovery Center
701 NE Sanchez Ave., Ocala
📞 (352) 401-3900
🌐 www.MyDiscoveryCenter.org
4. Don Garlits Museum of Drag Racing and International Drag Racing Hall of Fame
13700 SW 16th Ave., Ocala
📞 (877) 271-3278
🌐 www.Garlits.com
5. Florida Carriage Museum (at Grand Oaks)
3000 Marion County Rd., Weirsdale
📞 (352) 750-5500
🌐 www.TheGrandOaks.com
6. Florida Thoroughbred Breeders & Owners Association Museum & Art Gallery
801 SW 60th Ave., Ocala
📞 (352) 629-2160
🌐 www.FTBOA.com
7. Marion County’s Museum of History & Archaeology
307 SE 26th Ter., Ocala
📞 (352) 236-5245
🌐 www.MarionCountyArchaeology.com / MCMEA
8. Ocala Model Railroaders
1247 NE 3rd St., Ocala
📞 (352) 401-0747
(Call for Hours of Operation)
🌐 www.OcalaModelRailroaders.com
9. Silver River Museum
1445 NE 58th Ave., Ocala
📞 (352) 236-5401
🌐 www.SilverRiverMuseum.com
10. Webber Center Gallery
3001 SW College Rd., Ocala
📞 (352) 873-5809
🌐 www.CF.edu

PERFORMING ARTS
1. College of Central Florida Theatre
3001 SW College Rd., Ocala
📞 (352) 873-5810
🌐 www.CF.edu
2. Marion Ballet Theatre
1713 SW 17th St., Ocala
📞 (352) 629-6155
🌐 www.MarionPerformingBallet.org
3. Ocala Civic Theatre
4337 E. Silver Springs Blvd., Ocala
📞 (352) 236-2274
🌐 www.OcalaCivicTheatre.com
4. Ocala Symphony Orchestra
820 SE Ft. King St., Ocala
📞 (352) 351-1606
🌐 www.OcalaSymphony.com


CATEGORIA 3 — BOATING & FISHING
1. Carney Island Recreation & Conservation Area, Lake Weir
14215 SE 115th Ave., Ocklawaha
📞 (352) 671-8560
2. Eureka East & West Boat Ramps, Ocklawaha River
East: 15698 NE 152nd Street, Ft. McCoy
West: 15968 NE 154th Street, Ft. McCoy
📞 (352) 671-8560
3. Gores Landing Boat Ramp, Ocklawaha River
13800 NE 98th St., Ft. McCoy
📞 (352) 671-8560
4. Heagy Burry Park Boat Ramp, Orange Lake
5040 NW 191st Street Rd., Orange Lake
📞 (352) 671-8560
5. Hope Boat Ramp, Lake Weir
11060 SE 115th Ave., Weirsdale
📞 (352) 671-8560
6. KP Hole Park Boat Ramp, Rainbow River
9435 SW 190th Avenue Rd., Dunnellon
📞 (352) 489-3055
🌐 www.KPHole.com
7. Lake Weir Boat Rentals
12850 SE Hwy. 25, Ocklawaha
📞 (352) 288-1301
🌐 www.LakeWeirBoatRentals.com
8. Moss Bluff – North & South Boat Ramp, Ocklawaha River
North: 16298 SE 95th Pl., Ocklawaha
South: 16255 SE 95th Pl., Ocklawaha
📞 (352) 671-8560
9. Orange Springs Boat Ramp, Ocklawaha River
14620 NE 245th Street Rd., Orange Springs
📞 (352) 671-8560
10. Ray Wayside Park Boat Ramp (Ocala Boat Basin)
9560 NE 28th Ln., Silver Springs
📞 (352) 671-8560
11. Withlacoochee & Rainbow River Boat Ramp
Dunnellon City Hall, 20750 River Dr., Dunnellon
📞 (352) 732-1225

CATEGORIA 4 — EQUINE
EQUESTRIAN VENUES
1. Florida Horse Park
11008 S. Hwy. 475, Ocala
📞 (352) 307-6699
🌐 www.FLHorsePark.com
2. Grand Oaks Resort
3000 Marion County Rd., Weirsdale
📞 (352) 750-5500
🌐 www.TheGrandOaks.com
3. Ocala Breeders’ Sales
1701 SW 60th Ave., Ocala
📞 (352) 237-2154
🌐 www.OBSSales.com

HORSE FARM TOURS BY APPOINTMENT
1. Southeastern Livestock Pavilion
2232 NE Jacksonville Rd., Ocala
📞 (352) 671-8600
2. American Eagle Farm
8762 NW Hwy. 225A, Ocala
📞 (352) 895-8900
3. Bluffview Clydesdales/Friesians
1040 SE 59th St., Ocala
📞 (352) 861-7770
🌐 www.FriesianUSA.com
4. Bonheur Farm
1951 NW 114 Loop, Ocala
📞 (352) 427-7345
🌐 Facebook — BonheurFarm/Ocala
5. Bridlewood Farm
8318 NW 90th Ter., Ocala
(M–F 9:30 A.M.–3:00 P.M., Drive Thru, No Tours)
📞 (352) 622-5319
🌐 www.BridlewoodFarm.com
6. Buena Vista Farm
11122 W. Hwy. 326, Ocala
📞 (352) 622-9100
🌐 www.BuenaVistaFarm.org
7. Cav-i Farm
13449 NW 82nd Street Rd., Ocala
📞 (352) 875-9686
🌐 www.Cav-i.com
8. Country Road Farm
8205 NW Hwy. 225, Ocala
📞 (352) 351-2040
🌐 www.Horsepital.com
9. Eddie Woods Stables
14840 W. Hwy. 40, Ocala
📞 (352) 489-8915
🌐 www.EddieWoods.com
10. Fogg Road Farm
12550 NW 110th Ave., Reddick
(8:00 A.M.–12:00 P.M.)
📞 (352) 266-8760
11. Goldmark Farm
5290 NW 130th Ave., Ocala
📞 (352) 369-3377
🌐 www.GoldmarkFarm.com
12. Grey Dawn Stables
201 SE 90th St., Ocala
📞 (352) 427-9721
🌐 www.GreyDawnStables.com
13. Gypsy Gold Farm
12501 SW 8th Ave., Ocala (Tours by Appt.)
📞 (352) 307-1999
🌐 www.GypsyGold.com
14. Hartley/De Renzo Thoroughbreds
6500 NW Hwy. 225A, Ocala
📞 (352) 732-8878
🌐 www.HartleyDeRenzo.com
15. HITS Post Time Farm
13710 US Hwy. 27, Ocala (January–March)
📞 (352) 620-2275
🌐 www.HITSShows.com
16. Journeyman Stud
5571 NW 100th St., Ocala
(9:00 A.M.–3:00 P.M.)
📞 (352) 629-1200
🌐 www.JourneymanBloodstock.com
17. Lone Palm Stables
6555 SW 66th St., Ocala
📞 (352) 598-4552
🌐 www.LonePalmStables.net
18. New England Shire Centre
4877 SW 134th Ter., Ocala
(Farm Tours for Groups of 20 or More by Reservation Only)
📞 (352) 873-3005
🌐 www.OcalaMarion.com/Partner/New-England-Shire-Center
19. Ocala Stud Farm
4400 SW 27th Ave., Ocala
(8:00 A.M.–3:00 P.M., 2:00–5:30 P.M.)
📞 (352) 237-2171
🌐 www.OcalaStud.com
20. Signature Stallions
7100 NW 110th St., Reddick
📞 (352) 369-1900
🌐 www.SignatureStallions.com
21. Superfine Farm
17250 SW 90th St., Ocala
📞 (352) 854-4556
22. The Equine Inn, LLC
13050 NW 97th Pl., Ocala
📞 (352) 433-3343
🌐 www.TheEquineInn.com
23. Twin Stars Equine, LLC
13729 NW 82nd Street Rd., Ocala
📞 (352) 209-5380
24. UF/IFAS Equine Sciences Center
2651 NW 100th St., Ocala
(10:00 A.M.–2:00 P.M.)
📞 (352) 222-8284
🌐 www.UFAL.edu
25. Winning Colors Paso Finos
5040 NW 110th Ave., Anthony
📞 (352) 622-1190
🌐 www.WinningColorsFinos.com
26. Woodside Ranch
11850 NE Hwy. 315, Ft. McCoy
📞 (352) 236-1076
27. Zoccolo De Danza
17321 SE 150th Avenue Rd., Weirsdale
📞 (352) 324-4581


CATEGORIA 5 — HORSEBACK RIDING & GUIDED TOURS
1. Cactus Jack’s Trail Rides
11150 SW 16th Ave., Ocala
📞 (352) 266-9326
🌐 www.CactusJacksTrailRides.com
2. Chasin’ A Dream Farm
9330 NW 110th Ave., Ocala (Tours by Appt.)
📞 (352) 208-3701
🌐 www.ChasinADream.com
3. Farm Tours of Ocala
801 SW 60th Ave., Ocala (Reservations)
📞 (352) 895-9302
🌐 www.FarmToursOfOcala.com
4. Happy Acres Ranch
10051 SW 125th Ter., Dunnellon
📞 (352) 489-8550
🌐 www.OcalaHappyAcres.com
5. Hidden Lark Farm
4990 SW 7th Ave Rd., Ocala (Trail Rides by Appt.)
📞 (352) 854-5151
🌐 www.HiddenLarkFarm.net
6. Horse Country Carriage Co. & Tours
5400 NW 110th Ave., Ocala (Horse Farm Tours by Carriage. Call for Reservations.)
📞 (352) 727-0900
🌐 www.HorseCountryCarriageCompanyAndTours.com
7. Makin’ Tracks
15901 NE 137th Ct., Ft. McCoy (Guided Trail Rides by Appt. Ocala National Forest)
📞 (352) 236-3299
🌐 www.OcalaTrails.com
8. North Star Acres
9950 SE 125th Ct., Dunnellon (Guided Trail Rides by Reservation Only. Call for Appt.)
📞 (352) 489-4761
🌐 www.DunnellonBusiness.com/NorthStar
9. The Canyons Zip Line & Canopy Tours / Horseback Riding
8045 NW Gainesville Rd., Ocala
📞 (352) 351-9477
🌐 www.ZipTheCanyons.com

CATEGORIA 6 — NATURE
1. Carney Island Recreation & Conservation Area
14215 SE 115th Ave., Ocklawaha
📞 (352) 671-8560
🌐 www.MarionCountyFL.org/Parks
2. Cross Florida Greenway – Santos Trailhead
3080 SE 80th St., Ocala
📞 (352) 236-7143
🌐 www.FloridaGreenwaysAndTrails.com
3. Cross Florida Greenway – Marshall Swamp Trailhead
4650 SE Maricamp Rd., Ocala
📞 (352) 236-7143
🌐 www.FloridaGreenwaysAndTrails.com
4. Cross Florida Greenway – Ray Wayside Park
9560 NE 28th Ln., Silver Springs
📞 (352) 236-7143
🌐 www.FloridaGreenwaysAndTrails.com
5. Cross Florida Greenway – Land Bridge Trailhead
11100 SW 16th Ave., Ocala
📞 (352) 236-7143
🌐 www.FloridaGreenwaysAndTrails.com
6. Cross Florida Greenway – 49th Ave. Trailhead
2135 NW 49th Ave., Ocala
🌐 www.FloridaGreenwaysAndTrails.com
7. Cross Florida Greenway – Pruitt Trailhead
15099 SW Hwy. 484, Dunnellon
🌐 www.FloridaGreenwaysAndTrails.com
8. Cross Florida Greenway – Ross Prairie Trailhead
10660 SW Hwy. 200, Dunnellon
📞 (352) 236-7143
🌐 www.FloridaGreenwaysAndTrails.com
9. Fort King National Historic Landmark
3925 E. Ft. King St., Ocala
📞 (352) 622-3244
🌐 www.FortKingOcala.com
10. Indian Lake State Forest Trailhead
1025 SE 150th Blvd., Silver Springs
📞 (352) 732-1225
🌐 www.FDACS.gov
11. Rainbow Springs State Park
19158 SW 81st Pl. Rd., Dunnellon
📞 (352) 465-8555
🌐 www.FloridaStateParks.org
12. Salt Springs Recreation Area
13851 N Hwy. 19, Salt Springs
📞 (352) 685-2048
🌐 www.Recreation.gov
13. Sholom Park
7110 SW 80th Ave., Ocala
📞 (352) 873-0848
🌐 www.SholomPark.com
14. Silver Springs State Park
5656 E Silver Springs Blvd., Silver Springs
📞 (352) 236-7148
🌐 www.SilverSprings.com
15. Silver River State Park Museum & Environmental Education Center
1445 NE 58th Ave., Ocala
📞 (352) 236-5401
🌐 www.SilverRiverMuseum.com
16. Venomous Reptile Teaching Facility – Gerold’s Snakes
11120 N. Magnolia Ave., Ocala
📞 (352) 612-1702
🌐 www.GeroldsSnakes.com

CATEGORIA 7 — WILDLIFE SANCTUARIES
1. Endangered Animal Rescue Sanctuary (EARS)
2615 E Hwy. 318, Citra
📞 (352) 732-3325
🌐 www.EARSInc.org
2. Forest Animal Rescue by Peace River Refuge & Ranch
Ocala National Forest — Tours by Appointment Only
📞 (352) 625-7377
🌐 www.ForestAnimalRescue.org
3. Kirby Family Farm
19630 NE 30th Street, Williston
📞 (352) 812-7435
🌐 www.KirbyFarm.com
4. Octagon Wildlife Sanctuary
41660 SW 36th Ter., Punta Gorda
📞 (941) 575-4343
🌐 www.OctagonWildlife.org
5. The Canyons Zip Line & Adventure Park – Wildlife Area
8045 NW Gainesville Rd., Ocala
📞 (352) 351-9477
🌐 www.ZipTheCanyons.com
(Este aparece tanto em aventuras quanto em áreas de natureza.)
1. The Petting Zoo Ocala
11150 SW 93rd Ct Rd., Ocala
📞 (352) 789-0813
🌐 Facebook: The Petting Zoo Ocala
2. The Butterfly Rainforest (Florida Museum of Natural History)
3215 Hull Rd., Gainesville
📞 (352) 846-2000
🌐 www.FloridaMuseum.ufl.edu


CATEGORIA 8 — RENTALS & CHARTERS
1. Angell’s Mobile Marine Canvas
12385 SE 110th Ave., Belleview
📞 (352) 245-1861
🌐 Facebook: Angell’s Mobile Marine Canvas
2. Big Sun Skate Shop – Skateboard & Equipment Rentals
1220 SW 12th Street, Ocala
📞 (352) 236-6210
🌐 www.BigSunSkateShop.com
3. Blue Run Bicycles – Bike Rentals & Repairs
20799 Walnut St., Dunnellon
📞 (352) 465-7535
🌐 www.BlueRunBicycles.com
4. Cactus Jack’s Trail Rides – Horseback Riding / Guided Tours
11150 SW 16th Ave., Ocala
📞 (352) 266-9326
🌐 www.CactusJacksTrailRides.com
(Também listado em Horseback Riding & Guided Tours.)
1. Discovery Bicycle Tours
8045 NW Gainesville Rd., Ocala
📞 (800) 257-2226
🌐 www.DiscoveryBicycleTours.com
2. Florida Horse Park – Facility Rentals
11008 S. Hwy. 475, Ocala
📞 (352) 307-6699
🌐 www.FLHorsePark.com
(Para eventos, exposições e atividades equinas.)
1. Grand Oaks Resort – Carriage Rentals / Event Hosting
3000 Marion County Rd., Weirsdale
📞 (352) 750-5500
🌐 www.TheGrandOaks.com
2. Lake Weir Boat Rentals
12850 SE Hwy. 25, Ocklawaha
📞 (352) 288-1301
🌐 www.LakeWeirBoatRentals.com
3. Marion County Parks & Recreation – Park Rentals
111 SE 25th Ave., Ocala
📞 (352) 671-8560
🌐 www.MarionCountyFL.org/Parks
4. Ocala Bike Center – Bike Rentals & Tours
1504 E. Silver Springs Blvd., Ocala
📞 (352) 351-3475
🌐 www.OcalaBikeCenter.com
5. The Canyons Zip Line & Adventure Park – Horseback Riding / Zipline
8045 NW Gainesville Rd., Ocala
📞 (352) 351-9477
🌐 www.ZipTheCanyons.com
6. Wild Bills Airboat Tours – Airboat Adventures
12430 E Hwy. 40, Silver Springs
📞 (352) 726-6060
🌐 www.WildBillsAirboatTours.com
7. Blue Gator Tiki Bar & Boat Rentals
12189 S Williams St., Dunnellon
📞 (352) 465-1635
🌐 www.BlueGatorTiki.com


CATEGORIA 9 — CANOE & BOAT RENTALS
1. Adventure Outpost
30 NE 1st Ave., High Springs
📞 (386) 454-0611
🌐 www.AdventureOutpost.net
2. Angell’s Mobile Marine Canvas
12385 SE 110th Ave., Belleview
📞 (352) 245-1861
(Serviços de embarcações / suporte marítimo)
3. Blue Run of Dunnellon Park – Kayak & Tube Rentals (via concessionários locais)
19680 E Pennsylvania Ave., Dunnellon
📞 (352) 465-8510
🌐 Facebook: Blue Run of Dunnellon Park
4. Captain Bubba’s Airboat Tours & Rentals
8660 W. Hwy. 40, Ocala
📞 (352) 840-0111
🌐 Facebook: Captain Bubba’s
5. Florida Excursions (Kayak Rentals & Tours)
20629 W Pennsylvania Ave., Dunnellon
📞 (352) 214-4585
🌐 www.FloridaExcursions.com
6. KP Hole Park – Canoe, Kayak & Tube Rentals
9435 SW 190th Avenue Rd., Dunnellon
📞 (352) 489-3055
🌐 www.KPHole.com
7. Ocala Boat Rentals
(Serviços móveis — entrega e retirada)
📞 (352) 789-4954
🌐 www.OcalaBoatRental.com
8. Rainbow River Canoe & Kayak
12121 River View, Dunnellon
📞 (352) 489-7854
🌐 www.RainbowRiverCanoeAndKayak.com
9. Rainbow River Kayak Adventures
20729 River Dr., Dunnellon
📞 (352) 804-1573
🌐 www.RainbowRiverKayaking.com
10. Riverside Marina – Boat Rentals
2500 NE 95th St., Ocala
📞 (352) 622-5166
🌐 Facebook: Riverside Marina Ocala
11. Silver Springs State Park – Glass Bottom Boats & Kayak Rentals
5656 E Silver Springs Blvd., Silver Springs
📞 (352) 261-5840
🌐 www.SilverSprings.com
12. Swamp Fever Airboat Adventures
4110 SE Hwy. 484, Belleview
📞 (352) 508-5535
🌐 www.SwampFeverAirboat.com
13. The Blue Gator Tiki Bar & Boats
12189 S Williams St., Dunnellon
📞 (352) 465-1635
🌐 www.BlueGatorTiki.com
14. Discovery Kayak & Outdoor Center
8045 NW Gainesville Rd., Ocala
📞 (352) 789-4954
🌐 www.DiscoveryKayak.com


CATEGORIA 10 — CHARTERS
1. Captain Nick’s Merritt Island Charter Fishing
Merritt Island, FL — Offshore & Inshore Fishing Charters
📞 (321) 693-0898
🌐 www.CaptainNicksCharters.com
2. Captain Mike’s Lazy River Cruises
12189 S Williams St., Dunnellon (saída no Blue Gator Tiki Bar)
📞 (352) 637-2726
🌐 www.LazyRiverCruises.com
3. Captain Bob’s Airboat Tours
12430 E Hwy. 40, Silver Springs
📞 (352) 726-6060
🌐 www.WildBillsAirboatTours.com
(Operado junto ao Wild Bills)
4. Ocala Boat Rentals – Pontoon Boat Charters
Serviço móvel (Marion County & Lake Weir)
📞 (352) 789-4954
🌐 www.OcalaBoatRental.com
5. Withlacoochee River Cruises
12189 S Williams St., Dunnellon (saída no Blue Gator)
📞 (352) 637-2726
🌐 www.WithlacoocheeRiverCruises.com
6. Swamp Fever Airboat Adventures – Private Charters
4110 SE Hwy. 484, Belleview
📞 (352) 508-5535
🌐 www.SwampFeverAirboat.com
7. Captain Bubba’s Airboat Tours – Custom Charters
8660 W Hwy. 40, Ocala
📞 (352) 840-0111
🌐 Facebook: Captain Bubba’s Ocala
8. Sea Tow Crystal River – Boat Assistance & On-Water Support
Crystal River, FL
📞 (352) 794-6080
🌐 www.SeaTow.com
9. River Ventures – Manatee Swim & Pontoon Charters
498 SE Kings Bay Dr., Crystal River
📞 (352) 564-8687
🌐 www.SwimWithTheManatees.com
10. Captain Billy’s Crystal River Charters
12199 W Fort Island Trail, Crystal River
📞 (352) 665-5544
🌐 www.CrystalRiverFishingCharters.com
11. Marion County Parks – Boat Ramp Access for Private Charters
Countywide Facilities
📞 (352) 671-8560
🌐 www.MarionCountyFL.org/Parks
"""

def parse_data(raw):
    categories = []
    current_category = None
    places = []
    
    lines = raw.split('\n')
    
    current_place = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for Category
        cat_match = re.match(r'CATEGORIA \d+ — (.+)', line)
        if cat_match:
            current_category = cat_match.group(1).title()
            continue
            
        # Check for Subcategory (optional, we might just ignore or append to category)
        # But the prompt implies these are just headings. I'll ignore them for now or use them as part of the category?
        # The user said "CATEGORIA X - NAME". I'll stick to the main category.
        if line.isupper() and not line.startswith('CATEGORIA'):
            # It's a subheader like "ATV", "AMUSEMENTS". 
            # I will ignore it for the 'category' field to keep it simple as per user request "todas as categorias para elegir uma"
            continue
            
        # Check for Place Start "1. Name"
        place_match = re.match(r'^\d+\.\s+(.+)', line)
        if place_match:
            if current_place:
                places.append(current_place)
            
            name = place_match.group(1)
            current_place = {
                "id": re.sub(r'[^a-z0-9]', '-', name.lower()) + "-" + str(random.randint(1000, 9999)),
                "name": name,
                "category": current_category,
                "address": "",
                "phone": "",
                "website": "",
                "city": "Ocala", # Default
                "state": "FL",
                "lat": 29.1872 + (random.random() - 0.5) * 0.2, # Random jitter around Ocala
                "lng": -82.1401 + (random.random() - 0.5) * 0.2
            }
            continue
            
        # If we are inside a place, try to parse details
        if current_place:
            if line.startswith('📞'):
                current_place['phone'] = line.replace('📞', '').strip()
            elif line.startswith('🌐'):
                current_place['website'] = line.replace('🌐', '').strip()
            elif line.startswith('('):
                # Notes or hours, ignore for now or append to address?
                pass
            else:
                # Likely address
                # Try to extract city
                if ',' in line:
                    parts = line.split(',')
                    current_place['city'] = parts[-1].strip()
                    current_place['address'] = line
                else:
                    current_place['address'] = line

    if current_place:
        places.append(current_place)
        
    return places

places = parse_data(raw_data)
print(json.dumps(places, indent=2))
