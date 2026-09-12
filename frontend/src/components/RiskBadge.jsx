// frontend/src/components/RiskBadge.jsx
import React from 'react';

const RiskBadge = ({ score }) => {
  const getColor = (score) => {
    if (score > 0.7) return 'bg-red-100 text-red-800';
    if (score > 0.4) return 'bg-yellow-100 text-yellow-800';
    return 'bg-green-100 text-green-800';
  };
  const getLabel = (score) => {
    if (score > 0.7) return 'High Risk';
    if (score > 0.4) return 'Medium Risk';
    return 'Low Risk';
  };
  return (
    <span className={`px-2 py-0.5 rounded text-xs font-medium ${getColor(score)} focus-visible`}>
      {getLabel(score)} ({score.toFixed(2)})
    </span>
  );
};
export default RiskBadge;