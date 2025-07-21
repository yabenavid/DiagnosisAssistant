import React from "react";
import "../styles/admin/SegmentationTypeSelector.css";

const SegmentationTypeSelector = ({ selectedOption, setSelectedOption }) => {
    return (
        <div className="segmentation-type-selector">
            {/* <h4>Seleccione el tipo de Segementación:</h4> */}
            <div className="radio-group">
                <label>
                    <input
                        type="radio"
                        value="1"
                        checked={selectedOption === "1"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    Segment Anything (SAM)
                </label>
                <label>
                    <input
                        type="radio"
                        value="2"
                        checked={selectedOption === "2"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    Scikit-Image
                </label>
                 <label>
                    <input
                        type="radio"
                        value="3"
                        checked={selectedOption === "3"}
                        onChange={(e) => setSelectedOption(e.target.value)}
                    />
                    U-Net
                </label>
            </div>
        </div>
    );
};

export default SegmentationTypeSelector;
