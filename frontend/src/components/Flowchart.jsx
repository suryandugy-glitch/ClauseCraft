function Flowchart({ clauses, triplesPerClause, riskScores }) {
  return (
    <section className="my-6" aria-labelledby="clause-flow">
      <h2 id="clause-flow" className="text-xl font-semibold mb-3">Clause flow</h2>
      <ol className="space-y-2">
        {clauses.map((clause, index) => {
          const modalities = [...new Set(triplesPerClause[index].map(({ modality }) => modality))];
          return (
            <li key={index} className="border rounded-md p-3">
              <p className="font-semibold">Clause {index + 1}</p>
              <p>{clause}</p>
              <p className="text-sm">
                {[...modalities, riskScores[index] > 0.7 && 'Review flag'].filter(Boolean).join(' ? ')}
              </p>
            </li>
          );
        })}
      </ol>
    </section>
  );
}

export default Flowchart;
