import "./ImplementationRow.css";
import { useState } from "react";
import { DetailsButtonModal } from "../Modals/DetailsButtonModal";
import { mapLanguage } from "../../data/mapLanguage";
import { NavLink, useNavigate } from "react-router-dom";
import { Case, ImplementationData } from "../../data/parseReportData";

const ImplementationRow = ({
  cases,
  implementation,
}: {
  cases: Map<number, Case>;
  implementation: ImplementationData;
  key: number;
  index: number;
}) => {
  const [showDetails, setShowDetails] = useState(false);
  const navigate = useNavigate();
  const implementationPath = getImplementationPath(implementation);

  return (
    <tr>
      <th
        className="table-implementation-name align-middle p-0"
        onClick={() => navigate(`/implementations/${implementationPath}`)}
        scope="row"
      >
        <NavLink to={`/implementations/${implementationPath}`}>
          {implementation.metadata.name}
        </NavLink>
        <small className="text-muted ps-1">
          {mapLanguage(implementation.metadata.language)}
        </small>
      </th>
      <td className="align-middle d-none d-sm-table-cell">
        <small className="font-monospace text-muted">
          {implementation.metadata.version ?? ""}
        </small>
      </td>

      <td className="text-center align-middle">
        {implementation.erroredCases}
      </td>
      <td className="text-center align-middle">
        {implementation.skippedTests}
      </td>
      <td className="text-center align-middle details-required">
        {implementation.failedTests + implementation.erroredTests}
        <div className="hover-details text-center">
          <p>
            <b>failed</b>: &nbsp;{implementation.failedTests}
          </p>
          <p>
            <b>errored</b>: &nbsp;{implementation.erroredTests}
          </p>
        </div>
      </td>

      <td className="align-middle p-0">
        {implementation.failedTests +
          implementation.erroredTests +
          implementation.skippedTests >
          0 && (
          <button
            type="button"
            className="btn btn-sm btn-primary"
            onClick={() => setShowDetails(true)}
          >
            Details
          </button>
        )}
      </td>
      <DetailsButtonModal
        show={showDetails}
        handleClose={() => setShowDetails(false)}
        cases={cases}
        implementation={implementation}
      />
    </tr>
  );
};

const getImplementationPath = (implementation: ImplementationData) => {
  const pathSegment = implementation.id.split("/");
  return pathSegment[pathSegment.length - 1];
};

export default ImplementationRow;
