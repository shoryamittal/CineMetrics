/**
 * ECDIP - CinePulse AI Studio Copilot Engine
 * Client-Side Generative Strategic Reasoning System for OTT Executives
 */

class CinePulseCopilot {
  constructor(catalog) {
    this.catalog = catalog || [];
  }

  setCatalog(catalog) {
    this.catalog = catalog;
  }

  processQuery(rawQuery) {
    const query = rawQuery.toLowerCase().trim();

    // 1. Churn Defense / Post-Binge Cancellation Queries
    if (query.includes('churn') || query.includes('cancellation') || query.includes('retention') || query.includes('bridge')) {
      return this.handleChurnQuery();
    }

    // 2. Comparison Queries (Title vs Title)
    if (query.includes('vs') || query.includes('compare') || query.includes('versus') || query.includes('battle')) {
      return this.handleComparisonQuery(query);
    }

    // 3. Indian Cinema / Regional Hits
    if (query.includes('indian') || query.includes('bollywood') || query.includes('rrr') || query.includes('hindi') || query.includes('kgf')) {
      return this.handleIndianCinemaQuery();
    }

    // 4. Ad-Tier / AVOD Monetization Queries
    if (query.includes('ad') || query.includes('avod') || query.includes('cpm') || query.includes('advertising') || query.includes('commercial')) {
      return this.handleAdTierQuery();
    }

    // 5. Greenlight / Simulation Queries
    if (query.includes('greenlight') || query.includes('simulate') || query.includes('budget') || query.includes('acquire')) {
      return this.handleGreenlightQuery(query);
    }

    // 6. Contract Expiration / Cost Review
    if (query.includes('contract') || query.includes('cost') || query.includes('review') || query.includes('expire') || query.includes('renegotiate')) {
      return this.handleCostReviewQuery();
    }

    // Default intelligent overview
    return this.handleGeneralQuery(query);
  }

  handleChurnQuery() {
    const highRisk = this.catalog.filter(m => m.post_finale_vulnerability >= 30).slice(0, 3);
    const saveHeroes = this.catalog.filter(m => m.churn_defense_score >= 95).slice(0, 3);

    return {
      title: "🛡️ Churn Defense & Post-Binge Retention Analysis",
      text: `
        <p><strong>Executive Summary:</strong> The greatest threat to subscriber lifetime value (LTV) is post-finale cancellation. Viewers binge flagship series and churn within 72 hours if no algorithmic bridge is provided.</p>
        
        <h4 style="color: #f87171; margin-top: 10px;">⚠️ Highest Post-Finale Churn Vulnerability:</h4>
        <ul style="margin: 6px 0 12px 18px; font-size: 13px;">
          ${highRisk.map(m => `
            <li><strong>${m.title}</strong> (${m.genre}): <strong>${m.post_finale_vulnerability}%</strong> post-binge cancellation spike. <br><span style="color: #94a3b8;">Bridge Sequenced: ${m.bridge_titles ? m.bridge_titles.join(', ') : 'Catalog Sci-Fi'}</span></li>
          `).join('')}
        </ul>

        <h4 style="color: #34d399;">🛡️ Top 'Save' Anchors (High Churn Defense):</h4>
        <ul style="margin: 6px 0 12px 18px; font-size: 13px;">
          ${saveHeroes.map(m => `
            <li><strong>${m.title}</strong> — Churn Defense Index: <strong>${m.churn_defense_score}/100</strong> (Rewatch Rate: ${m.average_rewatch_rate}%)</li>
          `).join('')}
        </ul>

        <div style="background: rgba(0, 210, 255, 0.08); border-left: 3px solid #00d2ff; padding: 10px; border-radius: 4px; margin-top: 8px;">
          <strong>Strategic Recommendation:</strong> Deploy auto-cue 'Bridge Title' cards during the closing credits of <em>Stranger Things</em> and <em>Squid Game</em> to preserve an estimated <strong>₹185M ($2.2M)</strong> in recurring monthly subscription fees.
        </div>
      `,
      action: "VIEW_CHURN_TAB"
    };
  }

  handleComparisonQuery(query) {
    let t1 = this.catalog.find(m => m.title.toLowerCase().includes('inception')) || this.catalog[0];
    let t2 = this.catalog.find(m => m.title.toLowerCase().includes('interstellar')) || this.catalog[1];

    if (query.includes('stranger') && query.includes('bear')) {
      t1 = this.catalog.find(m => m.title.toLowerCase().includes('stranger')) || t1;
      t2 = this.catalog.find(m => m.title.toLowerCase().includes('bear')) || t2;
    } else if (query.includes('rrr') || query.includes('kgf')) {
      t1 = this.catalog.find(m => m.title.toLowerCase().includes('rrr')) || t1;
      t2 = this.catalog.find(m => m.title.toLowerCase().includes('k.g.f')) || this.catalog[2];
    }

    const winner = t1.content_roi > t2.content_roi ? t1 : t2;

    return {
      title: `⚔️ Head-to-Head Comparative Intelligence: ${t1.title} vs ${t2.title}`,
      text: `
        <table style="width: 100%; border-collapse: collapse; font-size: 12.5px; margin: 10px 0;">
          <thead>
            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); color: #94a3b8;">
              <th style="padding: 6px; text-align: left;">Strategic Vector</th>
              <th style="padding: 6px; text-align: right; color: #00d2ff;">${t1.title}</th>
              <th style="padding: 6px; text-align: right; color: #e50914;">${t2.title}</th>
            </tr>
          </thead>
          <tbody>
            <tr><td style="padding: 6px;">Total Revenue</td><td style="text-align: right; font-family: monospace;">₹${(t1.total_revenue/1e6).toFixed(0)}M</td><td style="text-align: right; font-family: monospace;">₹${(t2.total_revenue/1e6).toFixed(0)}M</td></tr>
            <tr><td style="padding: 6px;">Content ROI</td><td style="text-align: right; font-family: monospace; color: #34d399;">+${(t1.content_roi*100).toFixed(0)}%</td><td style="text-align: right; font-family: monospace; color: #34d399;">+${(t2.content_roi*100).toFixed(0)}%</td></tr>
            <tr><td style="padding: 6px;">Completion Rate</td><td style="text-align: right; font-family: monospace;">${t1.average_completion_rate}%</td><td style="text-align: right; font-family: monospace;">${t2.average_completion_rate}%</td></tr>
            <tr><td style="padding: 6px;">Churn Defense</td><td style="text-align: right; font-family: monospace;">${t1.churn_defense_score || 90}/100</td><td style="text-align: right; font-family: monospace;">${t2.churn_defense_score || 92}/100</td></tr>
            <tr><td style="padding: 6px;">Ad Yield CPM</td><td style="text-align: right; font-family: monospace;">$${t1.ad_yield_cpm || 32}/CPM</td><td style="text-align: right; font-family: monospace;">$${t2.ad_yield_cpm || 35}/CPM</td></tr>
          </tbody>
        </table>

        <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 10px; border-radius: 4px;">
          <strong>Executive Verdict:</strong> <strong>${winner.title}</strong> delivers superior capital efficiency (+${(winner.content_roi*100).toFixed(0)}% ROI) and broader global penetration. Recommend prioritizing marketing spend allocation toward ${winner.title}.
        </div>
      `,
      action: "VIEW_ARENA_TAB"
    };
  }

  handleIndianCinemaQuery() {
    return {
      title: "🇮🇳 Indian Cinema ROI & Pan-India Market Leadership",
      text: `
        <p><strong>Strategic Finding:</strong> Indian and Pan-India theatrical blockbusters deliver the single highest capital efficiency across our global streaming catalog, boasting an average portfolio ROI of <strong>+680%</strong> compared to the Western average of +195%.</p>
        
        <ul style="margin: 10px 0 14px 18px; font-size: 13px;">
          <li><strong>RRR</strong>: ₹920M Revenue vs ₹102M Cost &bull; <span style="color: #34d399; font-weight: 700;">+571% ROI</span> &bull; 78.4% Completion. High co-viewing across Western & Asian diaspora.</li>
          <li><strong>3 Idiots</strong>: ₹750M Revenue vs ₹29M Cost &bull; <span style="color: #34d399; font-weight: 700;">+1,729% ROI</span> &bull; 41.2% Rewatch Rate. Permanent evergreen catalog anchor.</li>
          <li><strong>K.G.F: Chapter 2</strong>: ₹860M Revenue vs ₹43M Cost &bull; <span style="color: #34d399; font-weight: 700;">+1,111% ROI</span>. Record-breaking day-1 streaming subscriber velocity.</li>
        </ul>

        <div style="background: rgba(0, 210, 255, 0.08); border-left: 3px solid #00d2ff; padding: 10px; border-radius: 4px;">
          <strong>Actionable Directive:</strong> Lock multi-year exclusive first-look SVOD output deals with Hombale Films, DVV Entertainment, and Excel Entertainment.
        </div>
      `,
      action: "FILTER_INDIAN_TITLES"
    };
  }

  handleAdTierQuery() {
    return {
      title: "💰 Hybrid AVOD & Ad-Tier Monetization Intelligence",
      text: `
        <p><strong>Macro Shift:</strong> Over <strong>48%</strong> of net new subscribers in 2025/2026 joined via the ad-supported tier. Ad revenue represents an incremental <strong>₹1.15 Billion ($13.8M)</strong> in high-margin cash flow.</p>
        
        <h4 style="color: #38bdf8; margin-top: 10px;">Top Advertising CPM Performers:</h4>
        <ul style="margin: 6px 0 12px 18px; font-size: 13px;">
          <li><strong>Squid Game</strong>: <strong>$46.00 CPM</strong> &bull; Total Ad Revenue: ₹410M ($4.9M)</li>
          <li><strong>Stranger Things</strong>: <strong>$44.00 CPM</strong> &bull; Total Ad Revenue: ₹340M ($4.0M)</li>
          <li><strong>Succession</strong>: <strong>$42.00 CPM</strong> (High affluent demographic appeal)</li>
          <li><strong>The Dark Knight</strong>: <strong>$41.50 CPM</strong> &bull; Ad Tolerance: 28 min intervals</li>
        </ul>

        <p style="font-size: 12.5px; color: #94a3b8;"><strong>Ad Tolerance Metric:</strong> Viewer churn begins when commercial load exceeds 4.5 minutes per hour. Optimal cue points are between minutes 24 and 38.</p>
      `,
      action: "VIEW_ADTIER_TAB"
    };
  }

  handleGreenlightQuery(query) {
    return {
      title: "🔮 AI Greenlight Capital Simulation",
      text: `
        <p><strong>Simulation Parameters:</strong> Proposed Production Budget: <strong>₹120,000,000 ($1.44M)</strong> with <strong>₹40,000,000</strong> Marketing in 15 Global Territories.</p>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin: 10px 0;">
          <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 4px;">
            <span style="font-size: 11px; color: #64748b;">Projected Views:</span>
            <div style="font-size: 15px; font-weight: 700; color: #fff;">14.8M</div>
          </div>
          <div style="background: rgba(255,255,255,0.03); padding: 8px; border-radius: 4px;">
            <span style="font-size: 11px; color: #64748b;">Predicted ROI:</span>
            <div style="font-size: 15px; font-weight: 700; color: #34d399;">+240.8%</div>
          </div>
        </div>

        <div style="background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; padding: 10px; border-radius: 4px;">
          <strong>AI Executive Verdict:</strong> <strong>APPROVED FOR GREENLIGHT</strong>. Strong capital hurdle clearance with 81.2% projected completion rate. Payback period estimated at 58 days.
        </div>
      `,
      action: "OPEN_SIMULATOR"
    };
  }

  handleCostReviewQuery() {
    return {
      title: "⚠️ Capital Rationalization & Contract Expirations",
      text: `
        <p><strong>Cost Audit Alert:</strong> 19,762 catalog titles are currently consuming capital above their revenue attribution velocity. Renegotiating these agreements unlocks up to <strong>₹340M ($4.1M)</strong> in annual savings.</p>

        <h4 style="color: #fbbf24; margin-top: 10px;">Primary Optimization Targets:</h4>
        <ul style="margin: 6px 0 12px 18px; font-size: 13px;">
          <li><strong>Ozark</strong>: Production cost ₹665K against low LTM rewatch &bull; <em>Action: Shift to ad-tier exclusive</em></li>
          <li><strong>Roma</strong>: High prestige licensing fee against mature reach &bull; <em>Action: Renegotiate 25% lower renewal tier</em></li>
          <li><strong>Money Heist</strong>: Heavy localization maintenance &bull; <em>Action: Bundle into Southern Europe regional package</em></li>
        </ul>
      `,
      action: "VIEW_PORTFOLIO_TAB"
    };
  }

  handleGeneralQuery(query) {
    return {
      title: "💡 CinePulse Strategic Intelligence Briefing",
      text: `
        <p>I am your <strong>CinePulse Studio Copilot</strong>. I synthesize real-time viewing velocity, financial return on capital, subscriber churn risk, and advertising yields across your 50,000 titles.</p>
        
        <p style="margin-top: 8px;"><strong>Suggested Strategic Queries:</strong></p>
        <div style="display: flex; flex-direction: column; gap: 6px; margin-top: 6px;">
          <button class="copilot-pill-btn" onclick="askCopilot('Which titles have the highest churn risk after finale?')">🛡️ Which titles have the highest post-finale churn risk?</button>
          <button class="copilot-pill-btn" onclick="askCopilot('Compare Inception vs Interstellar side-by-side')">⚔️ Compare Inception vs Interstellar side-by-side</button>
          <button class="copilot-pill-btn" onclick="askCopilot('How is our ad-supported tier performing?')">💰 How is our ad-supported tier performing?</button>
          <button class="copilot-pill-btn" onclick="askCopilot('What are our top performing Indian titles?')">🇮🇳 What are our top performing Indian titles?</button>
        </div>
      `,
      action: null
    };
  }
}

window.CinePulseCopilot = CinePulseCopilot;
