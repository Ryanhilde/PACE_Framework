package org.deidentifier.arx.examples;

/*
 * ARX: Powerful Data Anonymization
 * Copyright 2012 - 2021 Fabian Prasser and contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import org.deidentifier.arx.*;
import org.deidentifier.arx.criteria.KAnonymity;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

/**
 * This class implements an example on how to use the API by providing CSV files
 * as input.
 *
 * @author Fabian Prasser
 * @author Florian Kohlmayer
 * MODIFIED by Ryan Hildebrant
 */
public class ARXGeneralization_Resource_Country extends Example {

    /**
     * Entry point.
     *
     * @param args the arguments
     * @throws IOException
     */
    public static void main(String[] args) throws IOException {
        long count;
        int k = 10;
        try (Stream<Path> files = Files.list(Paths.get("C://Users//ryanh//OneDrive - San Diego State University " +
                "(SDSU.EDU)//SDSU Graduate Course Notes//Research//Papers//Code//Variants Resource Country//k = " + k))) {
            count = files.count();
        }
        for (long file = 0; file < count; file++) {
            try {
                Data data = Data.create("C://Users//ryanh//OneDrive - San Diego State University (SDSU.EDU)//" +
                        "SDSU Graduate Course Notes//Research//Papers//Code//Variants Resource Country//k = " + k + "//out_" + file + ".csv", StandardCharsets.UTF_8, ',');
                int columns = data.getHandle().getNumColumns();

                for (int i = 0; i < columns; i++) {
                    data.getDefinition().setAttributeType("resource country" + i, AttributeType.Hierarchy.create("C://Users//ryanh//" +
                            "OneDrive - San Diego State University (SDSU.EDU)//SDSU Graduate Course Notes//Research//" +
                            "Papers//Code//Hierarchies//resource_country_semantic.csv", StandardCharsets.UTF_8, ','));
                }

                ARXAnonymizer anonymizer = new ARXAnonymizer();

                ARXConfiguration config = ARXConfiguration.create();
                config.addPrivacyModel(new KAnonymity(k));
                // config.setSuppressionLimit(0.02d);
                config.setAlgorithm(ARXConfiguration.AnonymizationAlgorithm.BEST_EFFORT_BOTTOM_UP);
                ARXResult result = anonymizer.anonymize(data, config);
                result.getOutput(false).save("C://Users//ryanh//OneDrive - San Diego State University (SDSU.EDU)//" +
                        "SDSU Graduate Course Notes//Research//Papers//Code//Anonymized Resource Country//k = " + k + "//anonymized_data_"
                        + file + ".csv", ',');
            }
            catch (IllegalArgumentException ignored) {
                System.out.println(ignored);
            }
        }
    }
}
