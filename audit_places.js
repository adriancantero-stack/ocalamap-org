const fs = require('fs');
const https = require('https');

// 1. Extract Places from map.html
const html = fs.readFileSync('map.html', 'utf8');
const startTag = 'const places = [';
const startIndex = html.indexOf(startTag);
if (startIndex === -1) {
    console.error("Could not find places array");
    process.exit(1);
}

// Find the matching closing bracket (simple stack)
let open = 0;
let endIndex = -1;
for (let i = startIndex + startTag.length - 1; i < html.length; i++) {
    if (html[i] === '[') open++;
    if (html[i] === ']') {
        open--;
        if (open === 0) {
            endIndex = i + 1;
            break;
        }
    }
}

if (endIndex === -1) {
    console.error("Could not parse places array end");
    process.exit(1);
}

const placesStr = html.substring(startIndex + 'const places = '.length, endIndex);
// Use Function constructor to safely evaluate the array literal (handles trailing commas etc)
const places = new Function('return ' + placesStr)();

console.log(`Loaded ${places.length} places.`);

// 2. Geocode Helper
function geocode(place) {
    return new Promise((resolve) => {
        // Clean address: remove parenthetical notes
        const cleanAddress = place.address.replace(/<br>/g, ' ').replace(/\(.*?\)/g, '').trim();
        const query = encodeURIComponent(`${cleanAddress}, ${place.city}, ${place.state}`);

        const options = {
            hostname: 'nominatim.openstreetmap.org',
            path: `/search?format=json&q=${query}&limit=1`,
            headers: {
                'User-Agent': 'OcalaMapAudit/1.0 (adrian@example.com)'
            }
        };

        const req = https.get(options, (res) => {
            let data = '';
            res.on('data', (chunk) => data += chunk);
            res.on('end', () => {
                try {
                    const results = JSON.parse(data);
                    if (results.length > 0) {
                        resolve({
                            found: true,
                            lat: parseFloat(results[0].lat),
                            lng: parseFloat(results[0].lon),
                            display_name: results[0].display_name
                        });
                    } else {
                        resolve({ found: false });
                    }
                } catch (e) {
                    resolve({ found: false, error: e.message });
                }
            });
        });

        req.on('error', (e) => resolve({ found: false, error: e.message }));
    });
}

// 3. Distance Helper (Haversine)
function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2 - lat1);
    var dLon = deg2rad(lon2 - lon1);
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180)
}

// 4. Run Audit (Batch)
async function audit() {
    console.log("Starting audit (limit 10 for basic test)...");
    const discrepancies = [];

    // LIMIT TO 10 FOR TESTING to respect rate limits and time
    const limit = 10;
    let count = 0;

    for (const place of places) {
        if (count >= limit) break;

        // Skip if missing coords
        if (!place.lat || !place.lng) continue;

        process.stdout.write(`Checking ${place.name}... `);

        // Delay 1s (politeness)
        await new Promise(r => setTimeout(r, 1000));

        const result = await geocode(place);

        if (result.found) {
            const dist = getDistanceFromLatLonInKm(place.lat, place.lng, result.lat, result.lng);
            // Threshold: 0.5km (500 meters)
            if (dist > 0.5) {
                console.log(`\n⚠️  Mismatch (${dist.toFixed(2)}km)`);
                console.log(`   Current: ${place.lat}, ${place.lng}`);
                console.log(`   Found:   ${result.lat}, ${result.lng} (${result.display_name})`);
                discrepancies.push({
                    id: place.id,
                    name: place.name,
                    dist: dist.toFixed(2) + 'km',
                    current: { lat: place.lat, lng: place.lng },
                    suggested: { lat: result.lat, lng: result.lng }
                });
            } else {
                console.log("✅");
            }
        } else {
            console.log("❓ Not found");
        }
        count++;
    }

    console.log("\n--- Audit Report ---");
    console.log("Total Checked:", count);
    console.log("Discrepancies found:", discrepancies.length);
    if (discrepancies.length > 0) {
        fs.writeFileSync('audit_results.json', JSON.stringify(discrepancies, null, 2));
        console.log("Details saved to audit_results.json");
    }
}

audit();
