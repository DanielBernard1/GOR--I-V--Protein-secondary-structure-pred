CREATE TABLE alignments(
    alignment_id INT,
    pdb_id VARCHAR(20),
    PRIMARY KEY (alignment_id, pdb_id)
);

INSERT INTO alignments 
SELECT t2.alignment_id, t2.pdb_id 
FROM alignment_sequences t2;