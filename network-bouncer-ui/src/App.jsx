import { useState } from 'react';
import threatData from './threat_feed.json';
import { ShieldAlert, ShieldCheck, Activity, Database, Search } from 'lucide-react';

export default function App() {
  const [searchTerm, setSearchTerm] = useState('');

  // Calculate live stats for the top cards
  const totalThreats = threatData.length;
  const criticalThreats = threatData.filter(t => t.severity === 'CRITICAL').length;
  const exfilRisks = threatData.filter(t => t.exfiltration_risk).length;

  // Filter the table based on search input
  const filteredThreats = threatData.filter(threat => 
    threat.srcip.includes(searchTerm) || threat.severity.includes(searchTerm.toUpperCase())
  );

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 p-8 font-sans">
      
      {/* Header */}
      <header className="flex justify-between items-center mb-8 border-b border-slate-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-white flex items-center gap-3">
            <ShieldAlert className="text-red-500 w-8 h-8" />
            The Network Bouncer
          </h1>
          <p className="text-slate-400 mt-1">Enterprise Threat Intelligence Dashboard | Team Gladiators</p>
        </div>
        <div className="flex items-center gap-2 bg-slate-800 px-4 py-2 rounded-lg text-sm text-slate-300">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          Live Feed Active
        </div>
      </header>

      {/* KPI Stat Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Total Flagged IPs</p>
              <h2 className="text-3xl font-bold mt-2">{totalThreats}</h2>
            </div>
            <Activity className="text-blue-400 w-6 h-6" />
          </div>
        </div>
        
        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Critical Threats</p>
              <h2 className="text-3xl font-bold mt-2 text-red-400">{criticalThreats}</h2>
            </div>
            <ShieldAlert className="text-red-400 w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Data Exfiltration Risks</p>
              <h2 className="text-3xl font-bold mt-2 text-orange-400">{exfilRisks}</h2>
            </div>
            <Database className="text-orange-400 w-6 h-6" />
          </div>
        </div>

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-slate-400 text-sm font-medium">Network Status</p>
              <h2 className="text-xl font-bold mt-2 text-emerald-400 mt-3">Mitigation Active</h2>
            </div>
            <ShieldCheck className="text-emerald-400 w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Data Table Section */}
      <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-lg overflow-hidden">
        <div className="p-6 border-b border-slate-700 flex justify-between items-center bg-slate-800/50">
          <h3 className="text-lg font-semibold">Active Threat Log</h3>
          
          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-slate-400 w-4 h-4" />
            <input 
              type="text" 
              placeholder="Search IPs or Severity..."
              className="bg-slate-900 border border-slate-700 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-blue-500 w-64 text-slate-200"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-900/50 text-slate-400">
              <tr>
                <th className="px-6 py-4 font-medium">Source IP</th>
                <th className="px-6 py-4 font-medium">Severity</th>
                <th className="px-6 py-4 font-medium text-right">Ports Scanned</th>
                <th className="px-6 py-4 font-medium text-right">Data Exfiltrated</th>
                <th className="px-6 py-4 font-medium text-center">Targeted Infra</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {filteredThreats.map((threat, idx) => (
                <tr key={idx} className="hover:bg-slate-700/30 transition-colors">
                  <td className="px-6 py-4 font-mono text-slate-200">{threat.srcip}</td>
                  <td className="px-6 py-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wider
                      ${threat.severity === 'CRITICAL' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 
                        threat.severity === 'High' ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30' : 
                        'bg-blue-500/20 text-blue-400 border border-blue-500/30'}`}>
                      {threat.severity.toUpperCase()}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right font-mono text-slate-300">
                    {threat.unique_dst_ports.toLocaleString()}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <span className={`font-mono ${threat.exfiltration_risk ? 'text-red-400 font-bold' : 'text-slate-300'}`}>
                      {(threat.total_bytes_sent / 1024 / 1024).toFixed(2)} MB
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    {threat.critical_targets ? 
                      <span className="text-red-400 text-xs font-bold bg-red-400/10 px-2 py-1 rounded">🚨 YES</span> : 
                      <span className="text-slate-500">—</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredThreats.length === 0 && (
            <div className="p-8 text-center text-slate-500">
              No threats match your search criteria.
            </div>
          )}
        </div>
      </div>

    </div>
  );
}