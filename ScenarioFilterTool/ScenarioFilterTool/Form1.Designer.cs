namespace ScenarioFilterTool
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.btnOpen = new System.Windows.Forms.Button();
            this.openFileDialog1 = new System.Windows.Forms.OpenFileDialog();
            this.groupBox2 = new System.Windows.Forms.GroupBox();
            this.cbPart = new System.Windows.Forms.ComboBox();
            this.label3 = new System.Windows.Forms.Label();
            this.cbVariation = new System.Windows.Forms.ComboBox();
            this.label2 = new System.Windows.Forms.Label();
            this.label1 = new System.Windows.Forms.Label();
            this.cbTargetWord3 = new System.Windows.Forms.ComboBox();
            this.cbTargetWord2 = new System.Windows.Forms.ComboBox();
            this.cbTargetWord1 = new System.Windows.Forms.ComboBox();
            this.lblTarget2 = new System.Windows.Forms.Label();
            this.lblTarget1 = new System.Windows.Forms.Label();
            this.groupBox3 = new System.Windows.Forms.GroupBox();
            this.btnSave = new System.Windows.Forms.Button();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.groupBox1.SuspendLayout();
            this.groupBox2.SuspendLayout();
            this.groupBox3.SuspendLayout();
            this.SuspendLayout();
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.btnOpen);
            this.groupBox1.Location = new System.Drawing.Point(12, 12);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(418, 87);
            this.groupBox1.TabIndex = 0;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "1. Open the Interaction Manager JSON file";
            // 
            // btnOpen
            // 
            this.btnOpen.Location = new System.Drawing.Point(24, 28);
            this.btnOpen.Name = "btnOpen";
            this.btnOpen.Size = new System.Drawing.Size(164, 46);
            this.btnOpen.TabIndex = 0;
            this.btnOpen.Text = "Open JSON file...";
            this.btnOpen.UseVisualStyleBackColor = true;
            this.btnOpen.Click += new System.EventHandler(this.btnOpen_Click);
            // 
            // openFileDialog1
            // 
            this.openFileDialog1.FileName = "openFileDialog1";
            this.openFileDialog1.Filter = "JSON files|*.json";
            this.openFileDialog1.RestoreDirectory = true;
            // 
            // groupBox2
            // 
            this.groupBox2.Controls.Add(this.cbPart);
            this.groupBox2.Controls.Add(this.label3);
            this.groupBox2.Controls.Add(this.cbVariation);
            this.groupBox2.Controls.Add(this.label2);
            this.groupBox2.Controls.Add(this.label1);
            this.groupBox2.Controls.Add(this.cbTargetWord3);
            this.groupBox2.Controls.Add(this.cbTargetWord2);
            this.groupBox2.Controls.Add(this.cbTargetWord1);
            this.groupBox2.Controls.Add(this.lblTarget2);
            this.groupBox2.Controls.Add(this.lblTarget1);
            this.groupBox2.Location = new System.Drawing.Point(12, 130);
            this.groupBox2.Name = "groupBox2";
            this.groupBox2.Size = new System.Drawing.Size(418, 309);
            this.groupBox2.TabIndex = 1;
            this.groupBox2.TabStop = false;
            this.groupBox2.Text = "2. Select the target words you want to include";
            // 
            // cbPart
            // 
            this.cbPart.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbPart.FormattingEnabled = true;
            this.cbPart.Items.AddRange(new object[] {
            "First",
            "Second"});
            this.cbPart.Location = new System.Drawing.Point(201, 265);
            this.cbPart.Name = "cbPart";
            this.cbPart.Size = new System.Drawing.Size(185, 24);
            this.cbPart.TabIndex = 11;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(21, 268);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(139, 17);
            this.label3.TabIndex = 3;
            this.label3.Text = "First or second part?";
            // 
            // cbVariation
            // 
            this.cbVariation.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbVariation.FormattingEnabled = true;
            this.cbVariation.Items.AddRange(new object[] {
            "Everything in L2",
            "Target words introduced in L1"});
            this.cbVariation.Location = new System.Drawing.Point(147, 220);
            this.cbVariation.Name = "cbVariation";
            this.cbVariation.Size = new System.Drawing.Size(239, 24);
            this.cbVariation.TabIndex = 10;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(21, 223);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(104, 17);
            this.label2.TabIndex = 9;
            this.label2.Text = "Variation L1/L2";
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(21, 144);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(96, 17);
            this.label1.TabIndex = 8;
            this.label1.Text = "Target word 3";
            // 
            // cbTargetWord3
            // 
            this.cbTargetWord3.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbTargetWord3.FormattingEnabled = true;
            this.cbTargetWord3.Location = new System.Drawing.Point(201, 141);
            this.cbTargetWord3.Name = "cbTargetWord3";
            this.cbTargetWord3.Size = new System.Drawing.Size(185, 24);
            this.cbTargetWord3.TabIndex = 4;
            // 
            // cbTargetWord2
            // 
            this.cbTargetWord2.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbTargetWord2.FormattingEnabled = true;
            this.cbTargetWord2.Location = new System.Drawing.Point(201, 91);
            this.cbTargetWord2.Name = "cbTargetWord2";
            this.cbTargetWord2.Size = new System.Drawing.Size(185, 24);
            this.cbTargetWord2.TabIndex = 3;
            // 
            // cbTargetWord1
            // 
            this.cbTargetWord1.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbTargetWord1.FormattingEnabled = true;
            this.cbTargetWord1.Location = new System.Drawing.Point(201, 38);
            this.cbTargetWord1.Name = "cbTargetWord1";
            this.cbTargetWord1.Size = new System.Drawing.Size(185, 24);
            this.cbTargetWord1.TabIndex = 2;
            // 
            // lblTarget2
            // 
            this.lblTarget2.AutoSize = true;
            this.lblTarget2.Location = new System.Drawing.Point(21, 94);
            this.lblTarget2.Name = "lblTarget2";
            this.lblTarget2.Size = new System.Drawing.Size(96, 17);
            this.lblTarget2.TabIndex = 1;
            this.lblTarget2.Text = "Target word 2";
            // 
            // lblTarget1
            // 
            this.lblTarget1.AutoSize = true;
            this.lblTarget1.Location = new System.Drawing.Point(21, 41);
            this.lblTarget1.Name = "lblTarget1";
            this.lblTarget1.Size = new System.Drawing.Size(96, 17);
            this.lblTarget1.TabIndex = 0;
            this.lblTarget1.Text = "Target word 1";
            // 
            // groupBox3
            // 
            this.groupBox3.Controls.Add(this.btnSave);
            this.groupBox3.Location = new System.Drawing.Point(12, 461);
            this.groupBox3.Name = "groupBox3";
            this.groupBox3.Size = new System.Drawing.Size(418, 93);
            this.groupBox3.TabIndex = 2;
            this.groupBox3.TabStop = false;
            this.groupBox3.Text = "3. Save the edited JSON file";
            // 
            // btnSave
            // 
            this.btnSave.Location = new System.Drawing.Point(24, 35);
            this.btnSave.Name = "btnSave";
            this.btnSave.Size = new System.Drawing.Size(164, 46);
            this.btnSave.TabIndex = 0;
            this.btnSave.Text = "Save JSON file...";
            this.btnSave.UseVisualStyleBackColor = true;
            this.btnSave.Click += new System.EventHandler(this.btnSave_Click);
            // 
            // saveFileDialog1
            // 
            this.saveFileDialog1.Filter = "JSON files|*.json";
            this.saveFileDialog1.RestoreDirectory = true;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(442, 566);
            this.Controls.Add(this.groupBox3);
            this.Controls.Add(this.groupBox2);
            this.Controls.Add(this.groupBox1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.MaximizeBox = false;
            this.Name = "Form1";
            this.Text = "Scenario filtering tool";
            this.groupBox1.ResumeLayout(false);
            this.groupBox2.ResumeLayout(false);
            this.groupBox2.PerformLayout();
            this.groupBox3.ResumeLayout(false);
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.GroupBox groupBox1;
        private System.Windows.Forms.Button btnOpen;
        private System.Windows.Forms.OpenFileDialog openFileDialog1;
        private System.Windows.Forms.GroupBox groupBox2;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.ComboBox cbTargetWord3;
        private System.Windows.Forms.ComboBox cbTargetWord2;
        private System.Windows.Forms.ComboBox cbTargetWord1;
        private System.Windows.Forms.Label lblTarget2;
        private System.Windows.Forms.Label lblTarget1;
        private System.Windows.Forms.ComboBox cbVariation;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.GroupBox groupBox3;
        private System.Windows.Forms.Button btnSave;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.Windows.Forms.ComboBox cbPart;
        private System.Windows.Forms.Label label3;
    }
}

