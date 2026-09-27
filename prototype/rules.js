// KISAN-EDGE advisory rule engine (prototype).
// Pure function: Observation -> Recommendation. No AI, no network.
// Mirrors RESEARCH_REPORT.md §5.1. Works in the browser and under node.
(function (root) {
  var SEV = { green: 0, amber: 1, red: 2 };
  function worse(a, b) { return SEV[a] >= SEV[b] ? a : b; }

  // obs: {disease, severe, conf, label_en, label_hi, treat_en, treat_hi,
  //       soil_vwc, air_temp_c, humidity_pct}
  function advise(obs) {
    // 1. Confidence gate — never advise on an unsure diagnosis.
    if (obs.disease && obs.conf < 0.70) {
      return { gate: true, conf: obs.conf };
    }
    var sev = 'green', en = [], hi = [], because = [];

    // 2. Disease action
    if (obs.disease) {
      sev = worse(sev, obs.severe ? 'red' : 'amber');
      en.push(obs.treat_en); hi.push(obs.treat_hi);
      because.push(obs.label_en + ' detected (' + Math.round(obs.conf * 100) + '%).');
    }
    // 3. Irrigation — FAO-56 MAD threshold (naive single-point).
    // ponytail: fixed 20/45% band, calibrate per soil/crop if it matters.
    if (obs.soil_vwc < 20) {
      sev = worse(sev, 'amber');
      en.push('Irrigate now — soil moisture is low.');
      hi.push('अभी सिंचाई करें — मिट्टी की नमी कम है।');
      because.push('Soil moisture ' + obs.soil_vwc + '% is below the 20% threshold.');
    } else if (obs.soil_vwc > 45) {
      sev = worse(sev, 'amber');
      en.push('Do not irrigate — soil is already saturated.');
      hi.push('सिंचाई न करें — मिट्टी पहले से संतृप्त है।');
      because.push('Soil moisture ' + obs.soil_vwc + '% is above the 45% waterlogging mark.');
    }
    // 4. Heat gate on spraying
    if (obs.disease && obs.air_temp_c > 36) {
      en.push('Spray in the early morning or evening — midday heat cuts effectiveness.');
      hi.push('सुबह जल्दी या शाम को छिड़काव करें — दोपहर की गर्मी असर घटाती है।');
      because.push('High temperature ' + obs.air_temp_c + '°C.');
    }
    // 5. Healthy and nothing else flagged
    if (!obs.disease && sev === 'green') {
      en.push('All good. Keep monitoring.');
      hi.push('सब ठीक है। निगरानी रखते रहें।');
    }
    return { gate: false, severity: sev, actions_en: en, actions_hi: hi, because: because };
  }

  root.advise = advise;
})(typeof window !== 'undefined' ? window : globalThis);

// --- self-check (runs only under node: `node rules.js`) ---
if (typeof require !== 'undefined' && typeof module !== 'undefined' && require.main === module) {
  var assert = require('assert');
  var A = globalThis.advise;
  var r1 = A({ disease: true, severe: true, conf: 0.92, treat_en: 'x', treat_hi: 'y',
               soil_vwc: 18, air_temp_c: 38 });
  assert.strictEqual(r1.severity, 'red');
  assert.strictEqual(r1.actions_en.length, 3);       // treat + irrigate + heat-timing
  assert.ok(r1.because.length >= 3);
  assert.strictEqual(A({ disease: true, conf: 0.54 }).gate, true);          // low conf gates
  var r3 = A({ disease: false, conf: 0.95, soil_vwc: 30, air_temp_c: 30 });
  assert.strictEqual(r3.gate, false);
  assert.strictEqual(r3.severity, 'green');
  assert.strictEqual(A({ disease: false, conf: 0.95, soil_vwc: 12, air_temp_c: 30 }).severity, 'amber');
  console.log('rules.js self-check: all assertions passed');
}
